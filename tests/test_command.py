import io
import shutil
import typing
from pathlib import Path

import pytest

from pre_commit_image.command import Command


@pytest.fixture()
def command() -> Command:
    return Command(stderr=io.StringIO(), stdout=io.StringIO())


def image_file_factory(
    extension: str,
) -> typing.Callable[[str], typing.Generator[str, None, None]]:
    def image_file_fixture(tmpdir: str) -> typing.Generator[str, None, None]:
        src = Path(__file__).parent.joinpath(f"fixtures/200x200.{extension}")
        dst = Path(tmpdir).joinpath(src.name)
        shutil.copy(src, dst)
        yield str(dst)
        if dst.exists():
            dst.unlink()

    return image_file_fixture


avif_image_file = pytest.fixture(image_file_factory("avif"))
heic_image_file = pytest.fixture(image_file_factory("heic"))
heif_image_file = pytest.fixture(image_file_factory("heif"))
jpg_image_file = pytest.fixture(image_file_factory("jpg"))
png_image_file = pytest.fixture(image_file_factory("png"))
svg_image_file = pytest.fixture(image_file_factory("svg"))
webp_image_file = pytest.fixture(image_file_factory("webp"))


def test_get_arguments_default(command: Command) -> None:
    args = command.get_arguments(["file1.jpg", "file2.png"])

    assert args["files"] == ["file1.jpg", "file2.png"]
    assert args["quality"] == 75
    assert args["threshold"] == 1024
    assert args["max_width"] is None
    assert args["max_height"] is None
    assert args["extension"] is None


def test_get_arguments_custom(command: Command) -> None:
    args = command.get_arguments([
        "file1.jpg",
        "file2.png",
        "--quality",
        "90",
        "--threshold",
        "2048",
        "--max-width",
        "1000",
        "--max-height",
        "800",
        "--extension",
        "webp",
    ])

    assert args["files"] == ["file1.jpg", "file2.png"]
    assert args["quality"] == 90
    assert args["threshold"] == 2048
    assert args["max_width"] == 1000
    assert args["max_height"] == 800
    assert args["extension"] == "webp"


def test_find_strategy(command: Command) -> None:
    jpg_strategy = command.find_strategy("test.jpg")
    png_strategy = command.find_strategy("test.png")

    assert jpg_strategy is not None
    assert png_strategy is not None
    assert jpg_strategy.name != png_strategy.name

    invalid_strategy = command.find_strategy("test.invalid")
    assert invalid_strategy is None


def test_handle_single_file(command: Command, jpg_image_file: str) -> None:
    src_size = Path(jpg_image_file).stat().st_size

    command.handle(
        files=[jpg_image_file],
        threshold=1024,
        quality=75,
        max_width=100,
        max_height=100,
        extension=None,
    )

    dst_size = Path(jpg_image_file).stat().st_size
    assert src_size > dst_size


def test_handle_with_extension_conversion(
    command: Command, jpg_image_file: str
) -> None:
    command.handle(
        files=[jpg_image_file],
        threshold=0,
        quality=75,
        max_width=None,
        max_height=None,
        extension="webp",
    )

    assert not Path(jpg_image_file).exists()
    assert Path(jpg_image_file).with_suffix(".webp").exists()


def test_handle_invalid_extension(
    command: Command, jpg_image_file: str
) -> None:
    command.handle(
        files=[jpg_image_file],
        threshold=1024,
        quality=75,
        max_width=None,
        max_height=None,
        extension="invalid",
    )

    assert Path(jpg_image_file).exists()
    assert not Path(jpg_image_file).with_suffix(".invalid").exists()


def test_run(command: Command, jpg_image_file: str) -> None:
    command.run([jpg_image_file, "--max-width", "100", "--max-height", "100"])
