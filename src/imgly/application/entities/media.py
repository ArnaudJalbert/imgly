from dataclasses import dataclass
from typing import Optional


@dataclass
class Media:
    """Media entity to store metadata of a media file.

    Attributes:
        title: The title of the media file.
        data: The base64 encoded data of the media file.
        description: Optional description of the media file.
    """

    title: str
    data: str
    description: Optional[str] = None
