from types import ModuleType
from pathlib import Path

from .absfactory import AbstractFactory
from .modules.base import BaseParser

class ParsersFactory(AbstractFactory[BaseParser]):
    modules_dir = Path(__file__).parent / "modules"
    parent_package = "src.parsers.modules"

    filter_files = ["__init__.py", "base.py"]

    @classmethod
    def get_class_name(cls, module: ModuleType):
        return next(
            filter(
                lambda x: x.endswith("Parser") and x != "BaseParser",
                dir(module),
            )
        )
    
    @classmethod
    def get_class_key(cls, class_: object) -> str:
        return getattr(class_, "domain")
