import asyncio
import re
from typing import Any

from pycep import services
from pycep.cep_data import CepData
from pycep.cep_service_loader import CepQueryServiceLoader
from pycep.exceptions import CepQueryError
from pycep.protocols.service_loader import CEPServicesLoader


class PyCEP:
    def __init__(
        self,
        cep: str,
        *,
        cep_services_loader: CEPServicesLoader,
        async_runner=asyncio,
        timeout: float = 10.0,
    ) -> None:
        self.__services = cep_services_loader.load()
        self.__async_runner = async_runner
        self.__timeout = timeout
        self.__tasks: list[asyncio.Task[Any]] = []
        self.__cep_data: CepData = CepData()
        self.__status: str = "waiting_query"
        self.__services and asyncio.run(self.__query_services(cep))

    def __create_tasks(self, cep: str) -> None:
        for service in self.__services:
            task = self.__async_runner.create_task(service.query_cep(cep))
            self.__tasks.append(task)

    async def __query_services(self, cep: str) -> None:
        cep = re.sub(r"\D", "", cep)
        self.__status = "querying"
        self.__create_tasks(cep)
        try:
            self.__cep_data = await self.__first_useful_result()
        finally:
            await self.__cancel_pending_tasks()
        self.__status = "query_done"

    async def __first_useful_result(self) -> CepData:
        """Wait for the first useful answer, whichever provider gives it.

        Providers run concurrently and none waits for another. Answers without
        data and failures are skipped, so a fast "not found" never hides a
        slower provider that has the CEP.

        Returns an empty CepData when at least one provider answered but none
        found the CEP.

        Raises:
            CepQueryError: If no provider answered (all failed or timed out).
        """
        pending = set(self.__tasks)
        answered = False
        deadline = asyncio.get_running_loop().time() + self.__timeout
        while pending:
            remaining = deadline - asyncio.get_running_loop().time()
            done, pending = await asyncio.wait(
                pending, timeout=max(remaining, 0), return_when=asyncio.FIRST_COMPLETED
            )
            if not done:
                break
            for task in done:
                if task.cancelled() or task.exception() is not None:
                    continue
                answered = True
                if task.result().is_useful():
                    return task.result()
        if not answered:
            raise CepQueryError("no provider could answer the CEP query")
        return CepData()

    async def __cancel_pending_tasks(self) -> None:
        for task in self.__tasks:
            not task.done() and task.cancel()
        await asyncio.gather(*self.__tasks, return_exceptions=True)

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
        timeout: float = 10.0,
    ) -> PyCEP:
        return PyCEP(
            cep=cep,
            cep_services_loader=cep_services_loader
            or CepQueryServiceLoader(module=services),
            timeout=timeout,
        )


Cep = CepFactory()
