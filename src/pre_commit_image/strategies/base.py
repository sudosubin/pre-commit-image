import typing

T = typing.TypeVar("T")


class BaseStrategy(typing.Protocol[T]):
    name: typing.ClassVar[str]
    extensions: typing.ClassVar[typing.List[str]]

    @staticmethod
    def is_strategy_available() -> bool: ...
    def open(self, path: str) -> typing.ContextManager[T]: ...
    def get_size(
        self, image: T
    ) -> typing.Union[typing.Tuple[int, int], typing.Tuple[None, None]]: ...
    def resize(self, image: T, width: int, height: int) -> T: ...
    def is_compress_available(self, image: T) -> bool: ...
    def compress(
        self, image: T, fp: typing.IO[bytes], quality: int
    ) -> None: ...
