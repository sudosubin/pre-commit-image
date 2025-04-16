import importlib.util
import typing

from PIL import Image, ImageFile

from pre_commit_image.strategies.base import BaseStrategy


class AVIFStrategy(BaseStrategy[Image.Image]):
    name: typing.ClassVar = "avif"
    extensions: typing.ClassVar = ["avif"]

    @staticmethod
    def is_strategy_available() -> bool:
        return importlib.util.find_spec("pillow_avif") is not None

    def open(self, path: str) -> ImageFile.ImageFile:
        import pillow_avif as pillow_avif

        return Image.open(path)

    def get_size(self, image: Image.Image) -> typing.Tuple[int, int]:
        return image.size

    def resize(
        self, image: Image.Image, width: int, height: int
    ) -> Image.Image:
        resample = Image.Resampling.LANCZOS
        return image.resize((width, height), resample, reducing_gap=3.0)

    def is_compress_available(self, image: Image.Image) -> bool:
        return isinstance(image, Image.Image)

    def compress(
        self, image: Image.Image, fp: typing.IO[bytes], quality: int
    ) -> None:
        import pillow_avif as pillow_avif

        image.save(fp, format="AVIF", speed=5, quality=quality)
