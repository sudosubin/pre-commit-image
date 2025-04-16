import dataclasses

from pre_commit_image.steps.compress import CompressStep
from pre_commit_image.steps.resize import ResizeStep
from pre_commit_image.steps.save import SaveStep


@dataclasses.dataclass()
class Steps:
    compress: CompressStep
    resize: ResizeStep
    save: SaveStep
