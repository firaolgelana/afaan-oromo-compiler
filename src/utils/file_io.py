"""UTF-8 file I/O helpers."""

from __future__ import annotations

from pathlib import Path

from pythoncompiler.paths import output_path_for as _output_path_for


def read_source(path: Path) -> str:
    """Read source file as UTF-8 text."""
    return path.read_text(encoding="utf-8")


def write_output(path: Path, content: str) -> None:
    """Write generated Python with UTF-8 encoding."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def output_path_for(
    source_path: Path,
    *,
    project_root: Path | None = None,
    is_entry: bool = True,
) -> Path:
    """Map .ao to .py under the project python/ folder (see pythoncompiler.paths)."""
    return _output_path_for(
        source_path, project_root=project_root, is_entry=is_entry
    )
