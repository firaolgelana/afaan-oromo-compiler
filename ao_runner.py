#!/usr/bin/env python3
"""
Run the .ao file whose path is in sys.argv[0] (used as executable shebang target).

Shebang on an .ao file (optional):
  #!/usr/bin/env python3 /path/to/local_lang_compiler/ao_runner.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from translator import compile_file


def main() -> int:
    script = Path(sys.argv[0])
    if script.suffix != ".ao":
        print("Dogoggora: Faayilii .ao barbaachisa.", file=sys.stderr)
        return 1
    return compile_file(script.resolve(), run_after=True, quiet=True)


if __name__ == "__main__":
    sys.exit(main())
