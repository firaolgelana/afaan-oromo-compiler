#!/usr/bin/env python3
"""
Run an .ao program in one step (transpile + execute).

Transpiles to python/ (like TypeScript outDir), then runs the generated .py.

Usage:
    python run.py path/to/program.ao

Shell alias (from this repo):
    alias aoc='python3 /path/to/afaan-oromo-lang/run.py'
    aoc test.ao
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from translator import compile_file


def main() -> int:
    if len(sys.argv) < 2:
        print("Itti fayyadama: python run.py <faayilii.ao>", file=sys.stderr)
        return 1
    return compile_file(Path(sys.argv[1]), run_after=True, quiet=True)


if __name__ == "__main__":
    sys.exit(main())
