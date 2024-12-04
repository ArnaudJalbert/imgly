from dataclasses import dataclass

from obsidian_media_upload.use_cases import UseCase
from obsidian_media_upload.entities import Media


class UploadMediaUseCase(UseCase):

    @dataclass(frozen=True)
    class UploadMediaInputDTO(UseCase.InputDTO):
        media_title: str
        media_data: bytes

    def execute(self, dto: UploadMediaInputDTO) -> None:
        media = Media(title=dto.media_title, data=dto.media_data.decode("utf-8"))

        self.repository.save(media)
