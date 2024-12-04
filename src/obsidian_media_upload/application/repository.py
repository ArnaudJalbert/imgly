from abc import ABC, abstractmethod

from obsidian_media_upload.entities import Media


class Repository(ABC):
    """An abstract class representing a repository for media files.

    This class is used to define the interface for a repository that can save and delete media files.
    Classes that implement this interface must implement the `save` and `delete` methods.
    """

    @classmethod
    @abstractmethod
    def save(cls, media: Media) -> None:
        """Saves a media file to the repository.

        Args:
            media: The media file to save.
        """

    @classmethod
    @abstractmethod
    def delete(cls, media: Media) -> None:
        """Deletes a media file from the repository.

        Args:
            media: The media file to delete.
        """
