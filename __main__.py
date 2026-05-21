"""Run: python -m local_lang_compiler program.ao [--run]  (from repo parent directory)"""

from __future__ import annotations

import sys
from pathlib import Path

_pkg = Path(__file__).resolve().parent
if str(_pkg) not in sys.path:
    sys.path.insert(0, str(_pkg))

from translator import main

if __name__ == "__main__":
    raise SystemExit(main())
