import contextlib
import importlib.util
import typing
from pathlib import Path

from pre_commit_image.strategies.base import BaseStrategy


class SVGStrategy(BaseStrategy[str]):
    name: typing.ClassVar = "svg"
    extensions: typing.ClassVar = ["svg"]

    @staticmethod
    def is_strategy_available() -> bool:
        return importlib.util.find_spec("scour") is not None

    @contextlib.contextmanager
    def open(self, path: str) -> typing.Generator[str, None, None]:
        yield Path(path).read_text(encoding="utf-8")

    def get_size(self, image: str) -> typing.Tuple[None, None]:
        return None, None

    def resize(self, image: str, width: int, height: int) -> str:
        return image

    def is_compress_available(self, image: str) -> bool:
        return isinstance(image, str)

    def compress(self, image: str, fp: typing.IO[bytes], quality: int) -> None:
        from scour import scour

        options = {
            "enable_viewboxing": True,
            "indent_type": "none",
            "remove_descriptive_elements": True,
            "shorten_ids": True,
            "strip_comments": True,
            "strip_ids": True,
        }
        fp.write(scour.scourString(image, options).encode("utf-8"))
