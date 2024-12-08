from dataclasses import dataclass
from typing import Optional

from .abstract_use_case import UseCase
from ..entities import Media


class UploadMediaUseCase(UseCase):

    @dataclass(frozen=True)
    class UploadMediaInputDTO(UseCase.InputDTO):
        media_title: str
        media_data: str
        media_description: Optional[str] = None

    def execute(self, dto: UploadMediaInputDTO) -> None:
        media = Media(
            title=dto.media_title,
            data=dto.media_data,
            description=dto.media_description,
        )

        self.repository.save(media)
