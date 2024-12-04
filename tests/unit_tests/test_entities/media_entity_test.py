from obsidian_media_upload.entities import Media


def test_create_media_entity():
    Media(title="test.jpg", data=bytes("test", "utf-8").decode("utf-8"))
