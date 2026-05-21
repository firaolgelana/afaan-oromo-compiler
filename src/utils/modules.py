"""Resolve and compile .ao modules (libraries)."""

from __future__ import annotations

from pathlib import Path

from .names import to_python_name


def python_module_name(ao_path: Path, *, is_entry: bool = False) -> str:
    """Python module name for an .ao file (libraries use _ao suffix)."""
    stem = to_python_name(ao_path.stem)
    if is_entry:
        return stem
    return f"{stem}_ao"


def normalize_import_spec(spec: str) -> str:
    """Turn import spec into a relative .ao path (e.g. math -> math.ao)."""
    spec = spec.strip().strip('"').strip("'")
    if not spec.endswith(".ao"):
        spec = f"{spec}.ao"
    return spec


def resolve_module_path(importer: Path, spec: str) -> Path:
    """
    Find an .ao file relative to the importing file.

    Search order:
      1. Same directory as importer
      2. lib/ subdirectory
    """
    rel = normalize_import_spec(spec)
    base = importer.resolve().parent
    candidates = [
        base / rel,
        base / "lib" / rel,
    ]
    for path in candidates:
        if path.is_file():
            return path.resolve()
    raise FileNotFoundError(rel)
