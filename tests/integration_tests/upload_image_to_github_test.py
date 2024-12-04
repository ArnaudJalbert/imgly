import base64
import os

from obsidian_media_upload.entities import Media
from obsidian_media_upload.github_infrastructure import GitHubRepository


def test_upload_image_to_github():
    repository = GitHubRepository()

    # Read the image file and encode it in base64
    current_directory = os.path.dirname(os.path.abspath(__file__))
    with open(
        os.path.join(current_directory, "test_data", "img.png"), "rb"
    ) as image_file:
        content = base64.b64encode(image_file.read()).decode("utf-8")

    media = Media("test_image_from_test.png", content)

    # Create the image file in the repository
    repository.save(media)
    repository.delete(media)
