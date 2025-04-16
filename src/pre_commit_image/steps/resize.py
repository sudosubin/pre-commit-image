import typing

from pre_commit_image.strategies.base import BaseStrategy

T = typing.TypeVar("T")


class ResizeStep:
    def __init__(self, *, stderr: typing.TextIO, stdout: typing.TextIO) -> None:
        self.stderr = stderr
        self.stdout = stdout

    def do(
        self,
        file: str,
        image: T,
        strategy: BaseStrategy[T],
        max_width: typing.Optional[int],
        max_height: typing.Optional[int],
    ) -> typing.Tuple[T, bool]:
        sizes = self.get_image_sizes(image, strategy, max_width, max_height)
        if sizes is None:
            return image, False

        self.stdout.write(
            f"[INFO] Resizing {file} from {sizes[0]}x{sizes[1]} to "
            f"{sizes[2]}x{sizes[3]}\n"
        )
        return strategy.resize(image, sizes[2], sizes[3]), True

    def get_image_sizes(
        self,
        image: T,
        strategy: BaseStrategy[T],
        max_width: typing.Optional[int],
        max_height: typing.Optional[int],
    ) -> typing.Optional[typing.Tuple[int, int, int, int]]:
        old_width, old_height = strategy.get_size(image)
        if old_width is None or old_height is None:
            return None

        new_width, new_height = old_width, old_height

        if max_width and max_height:
            ratio = min(max_width / old_width, max_height / old_height)
            new_width = int(old_width * ratio)
            new_height = int(old_height * ratio)
        elif max_width and max_height is None:
            new_width = max_width
            new_height = int(old_height * max_width / old_width)
        elif max_height and max_width is None:
            new_width = int(old_width * max_height / old_height)
            new_height = max_height

        if new_width >= old_width or new_height >= old_height:
            return None

        return old_width, old_height, new_width, new_height
