#!/usr/bin/env python3
"""
CLI entry point for the Afaan Oromoo -> Python transpiler.

Usage:
    python translator.py <source.ao>              # transpile to python/<source>.py
    python translator.py <source.ao> --run        # transpile, then execute
    python run.py <source.ao>                     # same as --run
    python -m local_lang_compiler <source.ao> --run   # from repo parent dir
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.compiler.project import ProjectCompiler
from src.errors.diagnostics import DiagnosticError


def compile_file(source_path: Path, *, run_after: bool = False, quiet: bool = False) -> int:
    """Transpile source_path (and fuudhu imports); optionally run the generated .py."""
    if not source_path.is_file():
        print(f"Dogoggora: Faayilii hin argamne: {source_path}", file=sys.stderr)
        return 1

    try:
        source_text = source_path.read_text(encoding="utf-8").strip()
        if not source_text:
            print(
                "Dogoggora: Faayiliin duwwaa dha. Barruu .ao kee barreessi (Save: Ctrl+S).",
                file=sys.stderr,
            )
            return 1

        compiler = ProjectCompiler()
        out_path = compiler.compile_entry(source_path)
        if not quiet:
            print(f"Milkaa'ina: {out_path}")

        if run_after:
            result = subprocess.run(
                [sys.executable, out_path.name],
                cwd=out_path.parent,
                check=False,
            )
            return result.returncode
        return 0
    except DiagnosticError as err:
        loc = ""
        if err.location:
            loc = f" (giddugaleessa {err.location.line}:{err.location.column})"
        print(f"{err.message}{loc}", file=sys.stderr)
        return 1
    except Exception as err:
        print(f"Dogoggora: {err}", file=sys.stderr)
        return 1


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Afaan Oromoo (.ao) to Python transpiler",
    )
    parser.add_argument("source", help="Path to a .ao source file")
    parser.add_argument(
        "--run",
        "-r",
        action="store_true",
        help="After transpiling, run the generated .py with Python",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="With --run, do not print the transpile success message",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    return compile_file(
        Path(args.source),
        run_after=args.run,
        quiet=args.quiet and args.run,
    )


if __name__ == "__main__":
    sys.exit(main())
