import argparse
import typing
from tempfile import SpooledTemporaryFile

from pre_commit_image.steps import Steps
from pre_commit_image.steps.compress import CompressStep
from pre_commit_image.steps.resize import ResizeStep
from pre_commit_image.steps.save import SaveStep
from pre_commit_image.strategies.avif import AVIFStrategy
from pre_commit_image.strategies.base import BaseStrategy
from pre_commit_image.strategies.heif import HEIFStrategy
from pre_commit_image.strategies.jpeg import JPEGStrategy
from pre_commit_image.strategies.png import PNGStrategy
from pre_commit_image.strategies.svg import SVGStrategy
from pre_commit_image.strategies.webp import WEBPStrategy
from pre_commit_image.utils.file import get_extension

T = typing.TypeVar("T")


class Command:
    def __init__(self, *, stderr: typing.TextIO, stdout: typing.TextIO) -> None:
        self.stderr = stderr
        self.stdout = stdout
        self.steps = Steps(
            compress=CompressStep(stderr=stderr, stdout=stdout),
            resize=ResizeStep(stderr=stderr, stdout=stdout),
            save=SaveStep(stderr=stderr, stdout=stdout),
        )
        self.strategies = self.get_strategies()

    def run(self, args: typing.Optional[typing.Sequence[str]] = None) -> None:
        arguments = self.get_arguments(args)
        return self.handle(**arguments)

    def handle(
        self,
        *,
        files: typing.List[str],
        threshold: int,
        quality: int,
        max_width: typing.Optional[int],
        max_height: typing.Optional[int],
        extension: typing.Optional[str],
    ) -> None:
        if extension:
            compress_strategy = self.find_strategy(f".{extension}")
            if compress_strategy is None:
                self.stderr.write(f"[WARN] {extension} extension is invalid\n")
                return
        else:
            compress_strategy = None

        for file in files:
            strategy = self.find_strategy(file)
            if strategy is None:
                self.stdout.write(f"[WARN] {file} is not a valid image file\n")
                continue

            self.handle_file(
                file=file,
                threshold=threshold,
                quality=quality,
                max_width=max_width,
                max_height=max_height,
                extension=extension,
                strategy=strategy,
                compress_strategy=compress_strategy or strategy,
            )

    def handle_file(
        self,
        *,
        file: str,
        threshold: int,
        quality: int,
        max_width: typing.Optional[int],
        max_height: typing.Optional[int],
        extension: typing.Optional[str],
        strategy: BaseStrategy,
        compress_strategy: BaseStrategy,
    ) -> None:
        with strategy.open(file) as image, SpooledTemporaryFile() as fp:
            image, is_resized = self.steps.resize.do(
                file, image, strategy, max_width, max_height
            )
            self.steps.compress.do(file, image, fp, compress_strategy, quality)
            self.steps.save.do(file, fp, threshold, extension, is_resized)

    def get_arguments(
        self, args: typing.Optional[typing.Sequence[str]] = None
    ) -> typing.Dict[str, typing.Any]:
        parser = argparse.ArgumentParser()
        parser.add_argument("files", nargs="*", help="File paths to process")
        parser.add_argument(
            "--quality",
            default=75,
            type=int,
            help="Quality to use for compress (default: %(default)s)",
        )
        parser.add_argument(
            "--threshold",
            default=1024,
            type=int,
            help="Minimum file size change to process in bytes",
        )
        parser.add_argument(
            "--max-width",
            type=int,
            help="Maximum width to resize image",
        )
        parser.add_argument(
            "--max-height",
            type=int,
            help="Maximum height to resize image",
        )
        parser.add_argument(
            "--extension",
            type=str,
            choices=self.strategies.keys(),
            help="Force output to a given extension with format",
        )
        return vars(parser.parse_args(args))

    def get_strategies(self) -> typing.Dict[str, BaseStrategy]:
        strategies: typing.List[BaseStrategy] = [
            strategy_class()
            for strategy_class in [
                AVIFStrategy,
                HEIFStrategy,
                JPEGStrategy,
                PNGStrategy,
                SVGStrategy,
                WEBPStrategy,
            ]
            if strategy_class.is_strategy_available()
        ]

        return {
            ext: strategy
            for strategy in strategies
            for ext in strategy.extensions
        }

    def find_strategy(self, path: str) -> typing.Optional[BaseStrategy]:
        if strategy := self.strategies.get(get_extension(path)):
            return strategy
        self.stderr.write(f"[WARN] No available strategy found for {path}\n")
        return None
