import typing

from PIL import Image, ImageFile, ImageOps

from pre_commit_image.strategies.base import BaseStrategy


class JPEGStrategy(BaseStrategy[Image.Image]):
    name: typing.ClassVar = "jpeg"
    extensions: typing.ClassVar = ["jpeg", "jpg"]

    @staticmethod
    def is_strategy_available() -> bool:
        return True

    def open(self, path: str) -> ImageFile.ImageFile:
        image = Image.open(path)
        ImageOps.exif_transpose(image, in_place=True)
        return image

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
        image.save(
            fp, format="JPEG", optimize=True, progressive=True, quality=quality
        )
