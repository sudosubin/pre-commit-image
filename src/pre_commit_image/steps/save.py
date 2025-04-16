import re
import typing
from pathlib import Path

from pre_commit_image.utils.file import get_extension, get_readable_byte_size

T = typing.TypeVar("T")


class SaveStep:
    def __init__(self, *, stderr: typing.TextIO, stdout: typing.TextIO) -> None:
        self.stderr = stderr
        self.stdout = stdout

    def do(
        self,
        file: str,
        fp: typing.IO[bytes],
        threshold: int,
        extension: typing.Optional[str],
        is_resized: bool,
    ) -> bool:
        source = Path(file) if isinstance(file, str) else file
        source_size = source.stat().st_size
        candidate_size = fp.tell()
        fp.seek(0)

        if is_resized or source_size - candidate_size > threshold:
            if extension and extension != get_extension(file):
                source.unlink()
                source = Path(source).with_suffix(f".{extension}")
                self.stdout.write(
                    f"[INFO] Renaming {file} → {source} with extension "
                    f"{extension}\n"
                )

            self.stdout.write(
                f"[INFO] Saving {file} "
                f"({get_readable_byte_size(source_size)} → "
                f"{get_readable_byte_size(candidate_size)})\n"
            )
            source.write_bytes(fp.read())
            return True

        self.stdout.write(
            f"[INFO] Skipping {file} "
            f"({get_readable_byte_size(source_size)} → "
            f"{get_readable_byte_size(candidate_size)})\n"
        )
        return False

    def get_image_path(self, file: str, extension: typing.Optional[str]) -> str:
        if extension:
            return re.sub(rf"\{get_extension(file)}$", f".{extension}", file)
        return file
