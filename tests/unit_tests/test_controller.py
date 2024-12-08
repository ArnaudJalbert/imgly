from unittest.mock import MagicMock

from imgly.application import Repository
from imgly.application.entities import Media
from imgly.controller import ImglyController


def test_upload_media():
    repository = MagicMock(spec=Repository)
    controller = ImglyController(repository=repository)
    dto = ImglyController.UploadMediaInputDTO(
        media_title="test.jpg", media_data="test", media_description="test_description"
    )

    controller.upload_media(dto)

    repository.save.assert_called_once()
    repository.save.assert_called_with(
        Media(title="test.jpg", data="test", description="test_description")
    )
