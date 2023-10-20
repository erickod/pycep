import importlib
from pkgutil import walk_packages
from types import ModuleType
from typing import Any, Callable

from pycep import services
from pycep.protocols.query_service import QueryService


class CepQueryServiceLoader:
    """Import all sub modules dinamically"""

    def __init__(
        self, module: ModuleType = services, walk_packages: Callable = walk_packages
    ) -> None:
        self._services: list[Any] = []
        self._module = module
        self._walk_packages = walk_packages

    def load(self) -> Any:
        for loader, module_name, is_pkg in self._walk_packages(
            self._module.__path__, self._module.__name__ + "."
        ):
            submodule = importlib.import_module(module_name)
            service = submodule.make()
            self.__is_compatible(service) and self._services.append(service)
        return self._services

    def __is_compatible(self, module: QueryService, raises: bool = True) -> bool:
        is_compatbile = isinstance(module, QueryService)
        if raises and not is_compatbile:
            raise TypeError(f"{module} must implement QueryService")
        return is_compatbile
