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


NATIVE_MODULES = {
    "herrega": "math",
    "yeroo": "time",
    "tasa": "random",
    "sirna": "os",
}

def is_native_module(spec: str) -> bool:
    """Check if an import spec corresponds to a Python standard library."""
    name = spec.strip().strip('"').strip("'")
    if name.endswith(".ao"):
        name = name[:-3]
    return name in NATIVE_MODULES

def native_module_for(spec: str) -> str:
    """Get the python module name for a native library."""
    name = spec.strip().strip('"').strip("'")
    if name.endswith(".ao"):
        name = name[:-3]
    return NATIVE_MODULES[name]


def resolve_module_path(importer: Path, spec: str) -> Path | None:
    """
    Find an .ao file relative to the importing file.
    Returns None if the spec is a native standard library.

    Search order:
      1. Same directory as importer
      2. lib/ subdirectory
    """
    if is_native_module(spec):
        return None

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
