#!/usr/bin/env python3
"""Check gallery thumbnails without touching full-size media."""

from __future__ import annotations

from pathlib import Path


THUMBNAIL_DIR = Path("gallery/thumbnail")
MAX_LONG_EDGE = 600
MAX_FILE_SIZE = 250 * 1024


def jpeg_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    index = 2
    while index < len(data):
        if data[index] != 0xFF:
            raise ValueError("invalid JPEG marker")
        marker = data[index + 1]
        index += 2
        if marker in {0xD8, 0xD9}:
            continue
        length = int.from_bytes(data[index : index + 2], "big")
        if marker in range(0xC0, 0xCF + 1) and marker not in {0xC4, 0xC8, 0xCC}:
            height = int.from_bytes(data[index + 3 : index + 5], "big")
            width = int.from_bytes(data[index + 5 : index + 7], "big")
            return width, height
        index += length
    raise ValueError("JPEG dimensions not found")


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("invalid PNG header")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def image_dimensions(path: Path) -> tuple[int, int]:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_dimensions(path)
    if suffix == ".png":
        return png_dimensions(path)
    raise ValueError(f"unsupported thumbnail format: {suffix}")


def main() -> int:
    errors: list[str] = []
    thumbnails = [
        path
        for path in sorted(THUMBNAIL_DIR.iterdir())
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    ]

    for path in thumbnails:
        width, height = image_dimensions(path)
        if max(width, height) > MAX_LONG_EDGE:
            errors.append(f"{path}: {width}x{height} exceeds {MAX_LONG_EDGE}px long edge")

        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            errors.append(f"{path}: {size} bytes exceeds {MAX_FILE_SIZE} byte thumbnail limit")

    if errors:
        print("Thumbnail audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Thumbnail audit passed for {len(thumbnails)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
