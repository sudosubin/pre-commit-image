import typing

from pre_commit_image.strategies.base import BaseStrategy

T = typing.TypeVar("T")


class CompressStep:
    def __init__(self, *, stderr: typing.TextIO, stdout: typing.TextIO) -> None:
        self.stderr = stderr
        self.stdout = stdout

    def do(
        self,
        file: str,
        image: T,
        fp: typing.IO[bytes],
        strategy: BaseStrategy[T],
        quality: int,
    ) -> bool:
        if not strategy.is_compress_available(image):
            self.stderr.write(
                f"[WARN] Compressing {file} with {strategy.name} "
                f"is not available\n",
            )
            return False

        strategy.compress(image, fp, quality)
        return True
