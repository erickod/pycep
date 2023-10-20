import asyncio
from typing import Any

from pycep import services
from pycep.cep_service_loader import CepQueryServiceLoader
from pycep.protocols.service_loader import CEPServicesLoader


class PyCEP:
    def __init__(
        self, cep: str, *, cep_services_loader: CEPServicesLoader, async_runner=asyncio
    ) -> None:
        self.__cep_number: str = cep
        self.__services = cep_services_loader.load()
        self.__async_runner = async_runner
        self.__tasks: list[asyncio.Task] = []
        self.__cep_data = None
        asyncio.run(self.__query_services(cep))

    async def __create_tasks(self, cep: str) -> Any:
        for service in self.__services:
            task = self.__async_runner.create_task(service.query_cep(cep))
            self.__tasks.append(task)

    async def __query_services(self, cep: str) -> Any:
        await self.__create_tasks(cep)
        await asyncio.wait(self.__tasks, return_when=asyncio.FIRST_COMPLETED)
        await self.__cancel_pending_tasks()

    async def __cancel_pending_tasks(self) -> None:
        for task in self.__tasks:
            task.done() and await self.__configure_cep_data(task)
            not task.done() and task.cancel()

    async def __configure_cep_data(self, task: asyncio.Task) -> None:
        if self.__cep_data:
            return
        self.__cep_data = task.result()

    def __int__(self) -> int:
        return int(self.__cep_number)


class CepFactory:
    def __call__(
        self,
        cep: str,
        *,
        cep_services_loader: CEPServicesLoader = CepQueryServiceLoader(module=services)
    ) -> PyCEP:
        return PyCEP(cep=cep, cep_services_loader=cep_services_loader)


Cep = CepFactory()
