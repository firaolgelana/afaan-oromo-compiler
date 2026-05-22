"""Map .ao sources to generated .py files under the project python/ folder."""

from __future__ import annotations

from pathlib import Path

OUTPUT_DIR = "python"


def find_project_root(start: Path) -> Path:
    """
    Project root: nearest ancestor with pyproject.toml or pythoncompiler/.

    Falls back to the source file's directory (single-file projects).
    """
    current = start.resolve()
    if current.is_file():
        current = current.parent
    markers = ("pyproject.toml", "pythoncompiler")
    for directory in (current, *current.parents):
        if any((directory / name).exists() for name in markers):
            return directory
    return current


def output_path_for(
    source_path: Path,
    *,
    project_root: Path | None = None,
    is_entry: bool = True,
) -> Path:
    """
    Map .ao to .py under python/ (TypeScript-style outDir).

    Entry scripts: foo.ao -> python/foo.py (mirrors folders under project root)
    Libraries (imported): math.ao -> python/math_ao.py
    """
    source_path = source_path.resolve()
    root = (project_root or find_project_root(source_path)).resolve()

    try:
        rel = source_path.relative_to(root)
    except ValueError:
        rel = Path(source_path.name)

    out_parent = root / OUTPUT_DIR / rel.parent
    out_parent.mkdir(parents=True, exist_ok=True)

    stem = rel.stem
    if is_entry:
        return out_parent / f"{stem}.py"
    return out_parent / f"{stem}_ao.py"
