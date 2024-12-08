from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from ..repository import Repository


class UseCase(ABC):
    """
    An abstract class representing a use case in the application.
    The use case is responsible for executing the business logic of the application.

    This class should be subclassed by concrete use cases that implement the `execute` method.
    Any input and output data transfer objects (DTOs) should be defined as nested classes and inherit the `InputDTO`
    and `OutputDTO` classes.

    The use case should only use the repository to interact with the data layer, it should not have any other external
    dependencies.

    Attributes:
        repository: A repository object that the use case uses to interact with the data layer.
    """

    @dataclass(frozen=True)
    class InputDTO:
        """
        A data transfer object (DTO) representing the input data for the use case.
        All input data should be passed to the use case through a subclass of this class.
        """

    @dataclass(frozen=True)
    class OutputDTO:
        """
        A data transfer object (DTO) representing the output data for the use case.
        All output data should be returned by the use case through a subclass of this class.
        """

    def __init__(self, repository: Repository) -> None:
        """
        Initializes the use case with the given repository.

        Args:
            repository: A repository object that the use case uses to interact with the data layer.
        """
        self.repository = repository

    @abstractmethod
    def execute(self, dto: InputDTO) -> Optional[OutputDTO]:
        """
        Executes the business logic of the use case with the given input data transfer object (DTO).
        This method should be implemented by concrete use cases and should be the only public method of the use case.
        Additional private methods can be defined to encapsulate the business logic further.

        Args:
            dto: The input data transfer object (DTO) for the use case.

        Returns:
            The output data transfer object (DTO) from the use case, or None if there is no output.
        """
