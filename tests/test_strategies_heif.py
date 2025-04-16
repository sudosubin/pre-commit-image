import shutil
import typing
from pathlib import Path
from tempfile import SpooledTemporaryFile

import pytest

from pre_commit_image.strategies.heif import HEIFStrategy


@pytest.fixture()
def image_file(tmpdir: str) -> typing.Generator[str, None, None]:
    src = Path(__file__).parent.joinpath("fixtures/200x200.heif")
    dst = Path(tmpdir).joinpath(src.name)
    shutil.copy(src, dst)
    yield str(dst)
    if dst.exists():
        dst.unlink()


def test_heif_strategy(image_file: str) -> None:
    strategy = HEIFStrategy()
    assert strategy.is_strategy_available()

    with strategy.open(image_file) as image:
        assert strategy.get_size(image) == (200, 200)

        image = strategy.resize(image, 100, 100)
        assert strategy.get_size(image) == (100, 100)

        with SpooledTemporaryFile() as fp:
            assert strategy.is_compress_available(image)
            strategy.compress(image, fp, 75)
            assert fp.tell() > 0
