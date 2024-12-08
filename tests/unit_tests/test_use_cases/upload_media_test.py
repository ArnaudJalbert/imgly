from unittest.mock import MagicMock

from imgly.application.entities import Media
from imgly.application.use_cases import UploadMediaUseCase


def test_media_upload_use_case():
    repository = MagicMock()
    use_case = UploadMediaUseCase(repository=repository)

    title = "test.jpg"
    data = "test"

    input_dto = UploadMediaUseCase.UploadMediaInputDTO(
        media_title=title, media_data=data
    )

    use_case.execute(input_dto)

    repository.save.assert_called_once()
    repository.save.assert_called_with(Media(title=title, data=data))
