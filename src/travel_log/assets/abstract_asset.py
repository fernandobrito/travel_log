import abc
import os
from dataclasses import dataclass
from functools import cached_property
from typing import TypeVar, Type

T = TypeVar('T', bound='AbstractAsset')


# Trick to enable type hinting on dataclass inheritance:
# from https://github.com/python/mypy/issues/5374#issuecomment-650656381
@dataclass
class _AbstractAsset(abc.ABC):
    path: str


class AbstractAsset(_AbstractAsset, abc.ABC):
    """
    Abstract asset grouping common properties and behavior for all assets.

    Object attributes:
        * path: absolute path to the file, including the filename

    Properties:
        * filename: the filename (extracted from the path)
        * allowed_extensions: a list of extensions allowed
    """

    @classmethod
    def from_folder_path(cls: Type[T], folder_path: str) -> list[T]:
        objects: list[T] = []

        for filename in os.listdir(folder_path):
            extension = filename.split('.')[-1]

            if extension in cls.allowed_extensions():
                objects.append(cls(os.path.join(folder_path, filename)))

        return objects

    @cached_property
    def filename(self) -> str:
        return os.path.basename(self.path)

    @classmethod
    @abc.abstractmethod
    def allowed_extensions(cls) -> list[str]:
        ...
