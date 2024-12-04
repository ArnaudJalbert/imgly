from abc import ABC, abstractmethod
from dataclasses import dataclass

from obsidian_media_upload.application import Repository


class UseCase(ABC):

    @dataclass(frozen=True)
    class InputDTO:
        pass

    @dataclass(frozen=True)
    class OutputDTO:
        pass

    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    @abstractmethod
    def execute(self, dto: InputDTO) -> OutputDTO:
        pass
