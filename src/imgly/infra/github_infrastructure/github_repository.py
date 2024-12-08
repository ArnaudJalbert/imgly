import json
import os
from datetime import datetime
from typing import Dict

import requests
from dotenv import load_dotenv
from requests import Response

from imgly.application.repository import Repository
from imgly.application.entities import Media


# load the environment variables, to get the GitHub token
load_dotenv()

REPO_NAME = "neighborly-celery"
MEDIA_FOLDER = "6-medias"


class UploadMediaError(Exception):
    """Raised when an error occurs while uploading a media file."""


class DuplicateMediaError(Exception):
    """Raised when a media file already exists in the repository."""


class DeleteMediaError(Exception):
    """Raised when an error occurs while deleting a media file."""


class GitHubRepository(Repository):
    """A class representing a repository that saves and deletes media files in a GitHub repository.

    This class implements the `Repository` interface and uses the GitHub API to save and delete media files.

    Attributes:
        headers: A dictionary containing the headers to be sent in the request.
        content_url: A string containing the URL to upload/delete media files to the repository.
    """

    # TODO (Arnaud) -> This should be provided at initialization and not hardcoded, maybe saved through a config file
    headers: Dict[str, str] = {
        "Authorization": f"token {os.environ['GH_TOKEN']}",
    }
    content_url: str = (
        "https://api.github.com/repos/ArnaudJalbert/{repo_name}/contents/{upload_path}"
    )

    @staticmethod
    def _get_path(media: Media) -> str:
        """Generates the path where the media file will be uploaded.

        Args:
            media: The media file to save.

        Returns:
            The path where the media file will be uploaded.
        """
        date: str = datetime.today().strftime("%Y-%m-%d")
        return f"{MEDIA_FOLDER}/{date}/{media.title}"

    @classmethod
    def save(cls, media: Media) -> None:
        """Saves a media file to the repository by uploading it to the GitHub repository.

        Args:
            media: The media file to save.

        Raises:
            UploadMediaError: An error occurred while uploading the media file.
            DuplicateMediaError: The media file already exists in the repository.
        """
        # generate the path where the media file will be uploaded
        upload_path: str = cls._get_path(media)

        # generate the commit message if the media file has does not have a description
        # if the media file has a description, use it as the commit message
        commit_message: str = (
            media.description
            if media.description
            else f"Add media file: {media.title} at {datetime.now()}"
        )

        # generate the url where the media file will be uploaded
        url: str = cls.content_url.format(repo_name=REPO_NAME, upload_path=upload_path)

        # check if the media file already exists in the repository
        retrieve_image: Response = requests.get(url, headers=cls.headers)

        # if the media file already exists, raise an error
        if retrieve_image.json().get("sha", False):
            raise DuplicateMediaError(
                f"Media file: {media.title} already exists in the repository."
            )

        # create the data to be sent in the request
        data: Dict[str, str] = {
            "message": commit_message,
            "content": media.data,
            "branch": "main",
        }

        save_media_response: Response = requests.put(
            url, headers=cls.headers, data=json.dumps(data)
        )

        if save_media_response.status_code >= 400:
            raise UploadMediaError(
                f"Failed to upload media file: {media.title} \n\n {save_media_response.text}"
            )

    @classmethod
    def delete(cls, media: Media) -> None:
        """Deletes a media file from the GitHub repository.
        Checks if the media file exists in the repository, then deletes it.

        Args:
            media: The media file to delete.

        Raises:
            DeleteMediaError: An error occurred while deleting the media file.
        """
        # generate the path where the media file will be deleted
        delete_path: str = cls._get_path(media)

        # generate the commit message if the media file has does not have a description
        # if the media file has a description, use it as the commit message
        commit_message: str = (
            media.description
            if media.description
            else f"Delete media file: {media.title} at {datetime.now()}"
        )

        # generate the url where the media file will be deleted
        url = cls.content_url.format(repo_name=REPO_NAME, upload_path=delete_path)

        # get the sha of the media file
        media_sha: str = requests.get(url, headers=cls.headers).json().get("sha")

        # if the media file does not exist, raise an error
        if not media_sha:
            raise DeleteMediaError(
                f"Media file: {media.title} does not exist in the repository, it can't be deleted."
            )

        # create the data to be sent in the request
        data: Dict[str, str] = {
            "message": commit_message,
            "branch": "main",
            "sha": media_sha,
        }

        delete_media_response: Response = requests.delete(
            url, headers=cls.headers, data=json.dumps(data)
        )

        if delete_media_response.status_code >= 400:
            raise DeleteMediaError(
                f"Failed to delete media file: {media.title} \n\n {delete_media_response.text}"
            )
