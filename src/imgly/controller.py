from dataclasses import dataclass, asdict
from typing import Optional

from imgly.application import Repository
from imgly.application.use_cases import UploadMediaUseCase


class ImglyController:
    """
    The ImglyController class is responsible for handling the business logic of the application.
    The controller interacts with the use cases and the repository to execute the required operations.
    It should be the only point of entry for the CLI or other interfaces to interact with the application, they should
    never use the use cases of entities directly.
    """

    @dataclass
    class UploadMediaInputDTO:
        """
        DTO for uploading media.

        Attributes:
            media_title: The title of the media.
            media_data: The base64 encoded media
            media_description: Optional description of the media file.
        """

        media_title: str
        media_data: str
        media_description: Optional[str] = None

    def __init__(self, repository: Repository) -> None:
        """
        Initializes the ImglyController.
        The repository needs to be passed in order to interact with the infrastructure.
        The repository should implement the Repository interface.

        Args:
            repository: The repository to interact with the infrastructure.
        """
        self.repository: Repository = repository

    def upload_media(self, dto: UploadMediaInputDTO) -> None:
        """
        Uploads media to the repository using the `UploadMediaUseCase`.
        A controller DTO is passed and will be used to create the use case DTO.

        Args:
            dto: The controller DTO containing the media title and base64 encoded media.

        Raises:
            UploadMediaError: If the media upload fails.
            DuplicateMediaError: If the media already exists in the repository.
        """
        # initialize the use case with the provided repository
        use_case = UploadMediaUseCase(repository=self.repository)

        # construct the use case DTO
        upload_use_case_dto: UploadMediaUseCase.UploadMediaInputDTO = (
            UploadMediaUseCase.UploadMediaInputDTO(**asdict(dto))
        )

        # execute the use case
        use_case.execute(upload_use_case_dto)
