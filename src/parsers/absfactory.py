import importlib
import logging
import os
from abc import ABC, abstractmethod
from functools import cache
from pathlib import Path
from types import ModuleType
from typing import Callable, Hashable, TypeVar, Generic

debug_logger = logging.getLogger("debug")

T = TypeVar("T")

CallableClass = Callable[..., T]


class AbstractFactory(Generic[T], ABC):
    """
    AbstractFactory
    ===============

    Class properties
    ----------------

    modules_dir: Path
        A path to dir with desired modules,
        which we want to get from our Factory.

    parent_package: str
        Full parent package path.
        Example: src.high_package.low_package

    filter_files: list[str]
        List of file names to filter from results.


    Required implemented methods
    ----------------------------
    @classmethod
    def get_class_name(cls, module: ModuleType) -> str:
        Prefer to use with dir(module)


    Available additional methods to overload
    ----------------------------------------
    @classmethod
    def get_class_key(cls, class_: object) -> Hashable:
        This value used to define key in our dictionary
        Default: class_.__class__.__name__
    """

    modules_dir: Path

    parent_package: str

    filter_files: list[str]

    @classmethod
    def get(cls, name: str) -> T:
        """
        Get class instance by class_name|key

        Arguments
        name: str
            A class name or a key, if defined by get_class_key-method

        Return
        Instance of class

        Exceptions
        ModuleNotFoundError
            Raises if module with given name was not found...
        """

        debug_logger.debug(f"Initialisation for: {name}")

        # Get class-object by it's name
        class_: CallableClass | None = cls.__get_classes_dict().get(name, None)

        if not class_:
            e = ModuleNotFoundError(f"Module with given name - {name} - not found!")
            debug_logger.exception(e)
            raise e

        return class_()

    @classmethod
    def exists(cls, name: str) -> bool:
        """
        Check if class with class_name|key exists in Factory.
        It's handy method if you do not want to catch exception of get-method.
        """

        class_: CallableClass | None = cls.__get_classes_dict().get(name, None)

        return class_ is not None

    @classmethod
    @cache
    def __get_classes_dict(cls) -> dict[Hashable, CallableClass]:
        """Get cached dictionary of all available classes by Factory"""

        classes_dict: dict[Hashable, CallableClass] = {}

        # Get all modules path in modules_dir folder
        for module_path in os.listdir(cls.modules_dir):
            # Filter unused, standard and all other modules,
            # which contains in our filter_files
            if module_path.endswith(".py") and module_path not in cls.filter_files:
                module: ModuleType = importlib.import_module(
                    ".%s" % module_path.removesuffix(".py"),
                    package=cls.parent_package,
                )

                # Get class_name by filtering all dir(module) data
                class_name = cls.get_class_name(module)

                class_ = getattr(module, class_name)
                classes_dict[cls.get_class_key(class_)] = class_

        return classes_dict

    @classmethod
    @abstractmethod
    def get_class_name(cls, module: ModuleType) -> str:
        """
        *In implementation of this method, I offer to use dir(module)*
        This method must return only name of the desired callable class.

        The reason behind this approach:
        All data got from dir(module) will have link to all of class Parents,
        methods, variables and etc., which contains in module,
        because of that, we need to carefully filter result.
        """

        ...

    @classmethod
    def get_class_key(cls, class_: object) -> Hashable:
        """This value used to define key in our dictionary"""

        return class_.__class__.__name__
