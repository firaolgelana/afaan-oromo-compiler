"""Shared identifier mapping for Python output."""


def to_python_name(name: str) -> str:
    """Map source identifiers to valid Python names (e.g. ida'uu -> ida_uu)."""
    return name.replace("'", "_")
