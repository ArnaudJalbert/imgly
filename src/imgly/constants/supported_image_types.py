from enum import Enum


class SupportedImageTypes(Enum):
    """
    Defines the supported image types.
    """

    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    TIFF = "tiff"


SUPPORTED_IMAGES_EXTENSIONS = [f".{e.value}" for e in SupportedImageTypes]
