"""UTF-8 file I/O helpers."""

from __future__ import annotations

from pathlib import Path


def read_source(path: Path) -> str:
    """Read source file as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def write_output(path: Path, content: str) -> None:
    """Write generated Python with UTF-8 encoding."""
    path.write_text(content, encoding="utf-8")


def output_path_for(source_path: Path, *, is_entry: bool = True) -> Path:
    """
    Map .ao to .py output.

    Entry scripts: foo.ao -> foo.py
    Libraries (imported): math.ao -> math_ao.py  (avoids stdlib name clashes)
    """
    if is_entry:
        return source_path.with_suffix(".py")
    return source_path.with_name(f"{source_path.stem}_ao.py")
