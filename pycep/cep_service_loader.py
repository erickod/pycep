import importlib
from pkgutil import walk_packages
from types import ModuleType
from typing import Any, Callable

from pycep import services


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
            service = importlib.import_module(module_name)
            self._services.append(service.make())
            return self._services
