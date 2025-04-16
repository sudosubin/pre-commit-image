import pytest

from pre_commit_image.utils.file import get_extension, get_readable_byte_size


@pytest.mark.parametrize(
    "path, expected",
    [
        ("/a/b/c/test.png", "png"),
        ("/a/b/c.temp/test.jpg", "jpg"),
        ("test.jpeg", "jpeg"),
        (".jpeg", "jpeg"),
    ],
)
def test_get_extension(path: str, expected: str) -> None:
    assert get_extension(path) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0 B"),
        (1023, "1,023 B"),
        (1024, "1 KiB"),
        (2200, "2.1 KiB"),
        (1024**2, "1 MiB"),
        (1024**3, "1 GiB"),
        (1024**4, "1 TiB"),
        (1024**5, "1,024 TiB"),
    ],
)
def test_get_readable_byte_size(value: int, expected: str) -> None:
    assert get_readable_byte_size(value) == expected
