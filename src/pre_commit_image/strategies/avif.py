import importlib.util
import typing

from PIL import Image, ImageFile

from pre_commit_image.strategies.base import BaseStrategy


def is_native_avif_available() -> bool:
    try:
        from PIL import AvifImagePlugin
    except ImportError:
        return False
    return bool(AvifImagePlugin.SUPPORTED)


def register_avif_plugin() -> None:
    if not is_native_avif_available():
        import pillow_avif as pillow_avif


class AVIFStrategy(BaseStrategy[Image.Image]):
    name: typing.ClassVar = "avif"
    extensions: typing.ClassVar = ["avif"]

    @staticmethod
    def is_strategy_available() -> bool:
        return (
            is_native_avif_available()
            or importlib.util.find_spec("pillow_avif") is not None
        )

    def open(self, path: str) -> ImageFile.ImageFile:
        register_avif_plugin()
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
        register_avif_plugin()
        image.save(fp, format="AVIF", speed=5, quality=quality)
