import asyncio
import re
from typing import Any

from pycep import services
from pycep.cep_data import CepData
from pycep.cep_service_loader import CepQueryServiceLoader
from pycep.protocols.service_loader import CEPServicesLoader


class PyCEP:
    def __init__(
        self, cep: str, *, cep_services_loader: CEPServicesLoader, async_runner=asyncio
    ) -> None:
        self.__services = cep_services_loader.load()
        self.__async_runner = async_runner
        self.__tasks: list[asyncio.Task[Any]] = []
        self.__cep_data: CepData = CepData()
        self.__status: str = "waiting_query"
        self.__services and asyncio.run(self.__query_services(cep))

    def __create_tasks(self, cep: str) -> Any:
        for service in self.__services:
            task = self.__async_runner.create_task(service.query_cep(cep))
            self.__tasks.append(task)

    async def __query_services(self, cep: str) -> Any:
        cep = re.sub(r"\D", "", cep)
        self.__status = "querying"
        self.__create_tasks(cep)
        self.__tasks and await asyncio.wait(
            self.__tasks, return_when=asyncio.FIRST_COMPLETED
        )
        self.__cancel_pending_tasks()
        self.__status = "query_done"

    def __cancel_pending_tasks(self) -> None:
        for task in self.__tasks:
            task.done() and self.__configure_cep_data(task)  # type: ignore
            not task.done() and task.cancel()

    def __configure_cep_data(self, task: asyncio.Task) -> None:
        self.__cep_data = task.result()

    def __getitem__(self, key: str | int) -> str | tuple[str, str]:
        if isinstance(key, int):
            return list(vars(self.__cep_data).items())[key]
        return self.__cep_data[key]

    @property
    def status(self) -> str:
        return self.__status

    @property
    def number(self) -> str:
        return self.__cep_data.cep

    @property
    def street(self) -> str:
        return self.__cep_data.street

    @property
    def district(self) -> str:
        return self.__cep_data.district

    @property
    def city(self) -> str:
        return self.__cep_data.city

    @property
    def state(self) -> str:
        return self.__cep_data.state

    @property
    def query_service(self) -> str:
        return self.__cep_data.provider

    def __repr__(self) -> str:
        return f"PyCEP(cep={self.__cep_data.cep})"


class CepFactory:
    def __call__(
        self,
        cep: str,
        *,
        cep_services_loader: CEPServicesLoader | None = None,
    ) -> PyCEP:
        return PyCEP(
            cep=cep,
            cep_services_loader=cep_services_loader
            or CepQueryServiceLoader(module=services),
        )


Cep = CepFactory()
