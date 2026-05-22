#!/usr/bin/env bash
# One-time setup after cloning the repo (Linux / macOS).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

if ! command -v python >/dev/null 2>&1; then
  echo "Dogoggora: python hin argamne. Python 3.10+ fe'i." >&2
  exit 1
fi

echo "==> Installing Afaan Oromoo transpiler (editable)..."
python -m pip install -e .

chmod +x ao run.py translator.py 2>/dev/null || true

echo ""
echo "Milkaa'ina! Run .ao programs with:"
echo "  aoc test.ao              # transpile + run (works from any folder)"
echo "  ao test.ao --run         # same via translator CLI"
echo "  python run.py test.ao   # without pip, from repo clone"
echo "  ./ao test.ao             # shell wrapper in this repo"
echo ""
echo "Cursor / VS Code syntax highlighting (optional):"
echo "  Open Extensions → install from folder → $REPO_ROOT/vscode-oromolang"
echo "  Then reload the window and open a .ao file."
echo ""
echo "Note: Shell aliases in ~/.bashrc are personal — this install adds"
echo "      global commands 'aoc' and 'ao' via pip (no manual alias needed)."
