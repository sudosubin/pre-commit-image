import sys

from pre_commit_image.command import Command


def main() -> None:
    command = Command(stderr=sys.stderr, stdout=sys.stdout)
    command.run(args=sys.argv[1:])


if __name__ == "__main__":
    main()
