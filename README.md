# pre-commit-image

[![version](https://badgen.net/github/release/sudosubin/pre-commit-image?label=version)](https://github.com/sudosubin/pre-commit-image/releases)
[![license](https://badgen.net/github/license/sudosubin/pre-commit-image?color=green)](LICENSE)

A command-line application that optimizes and resizes images, which can work as a git hook.
This command-line application can be invoked directly or using the configuration provided for the [pre-commit](https://pre-commit.com/). See below for more information.

## Supported Image Formats

Native supported formats: `jpeg`(`jpg`), `png`, `webp`

| Format |   Extra   |
|:------:|:---------:|
| `avif` | `.[avif]` |
| `heif` | `.[heif]` |
| `svg`  | `.[svg]`  |

`avif` is supported natively by Pillow 12 (Python 3.10+), so the `.[avif]` extra only installs [pillow-avif-plugin](https://github.com/fdintino/pillow-avif-plugin) on Python 3.8 and 3.9.

Python 3.8 to 3.15 are supported. Python 3.8 and 3.9 use older dependencies (Pillow 10.x, pillow-heif 0.18.x), while Python 3.10+ uses the latest ones.

## Usage

Add below to your project's `.pre-commit-config.yaml`.

```yaml
repos:
  - repo: https://github.com/sudosubin/pre-commit-image
    rev: v0.1.4
    hooks:
      - id: image
```

## Available arguments

For more diverse use cases, you can use the additional arguments below.

- **`--quality`**: Quality to use for compress (default: `75`)
- **`--threshold`**: Minimum file size change to process in bytes (default: `1024`)
- **`--max-width`**: Maximum width to resize image
  - This option will always resize and save the image if its width is greater than the value of that parameter.
- **`--max-height`**: Maximum height to resize image
  - This option will always resize and save the image if its height is greater than the value of that parameter.
- **`--extension`**: Force output to a given extension with format
  - This option reformats the image based on the image's extension and replaces the existing file with a new image file.

## Examples

Set the maximum width and height to `1200px`, and always save the image with the `AVIF` extension (and format).

```yaml
repos:
  - repo: https://github.com/sudosubin/pre-commit-image
    rev: v0.1.4
    hooks:
      - id: image
        args: [--max-width, "1200", --max-height, "1200", --extension, avif]
```
