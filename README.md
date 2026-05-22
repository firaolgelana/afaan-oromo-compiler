# Afaan Oromoo → Python

Write programs in **Afaan Oromoo** (`.ao` files); the transpiler compiles them to Python under `python/` and runs them.

```
.ao  →  Lexer  →  Parser  →  Code Generator  →  python/*.py  →  Python
```

**Requirements:** Python 3.10+

## Getting started (new users — after `git clone`)

GitHub only ships the **compiler and examples**. It does **not** copy your personal shell aliases or editor settings — each person runs setup once on their machine.

### Linux / macOS

```bash
git clone https://github.com/firaolgelana/afaan-oromo-lang.git
cd afaan-oromo-lang
./install.sh
```

### Windows

Use **PowerShell** (or Windows Terminal) in the cloned folder:

```powershell
git clone https://github.com/firaolgelana/afaan-oromo-lang.git
cd afaan-oromo-lang
.\install.ps1
```

| Windows environment | `./install.sh` | `.\install.ps1` | `pip install -e .` |
|---------------------|----------------|-----------------|----------------------|
| PowerShell / CMD | No | **Yes** | **Yes** |
| Git Bash | **Yes** | Yes | **Yes** |
| WSL (Ubuntu, etc.) | **Yes** | — | **Yes** |

Install [Python 3.10+](https://www.python.org/) and check **“Add python.exe to PATH”** during setup. If `aoc` is not found after install, open a **new** terminal window.

### After install (all platforms)

```bash
aoc path/to/program.ao
```

That installs **`aoc`** (run) and **`ao`** (compile) via pip. Manual install (same result):

```bash
pip install -e .
aoc test.ao
```

### What is not in the repo?

| On your PC only | In GitHub / clone |
|-----------------|-------------------|
| `alias aoc=...` in `~/.bashrc` | No — optional; `install.sh` replaces this |
| Nano/editor config | No |
| Generated `python/*.py` | No (built when you run `aoc`) |
| VS Code / Cursor colors | No — install highlighting once (below) |

### Syntax highlighting & colors (Cursor / VS Code)

Install **once** after clone. Reload the editor, then open a `.ao` file (language: **OromoLang**).

More detail: [`vscode-oromolang/README.md`](vscode-oromolang/README.md)

#### Option A — Symlink from your clone (Linux / macOS / Git Bash)

Replace the path with **where you cloned** the repo, then run:

```bash
ln -s /path/to/afaan-oromo-lang/vscode-oromolang ~/.cursor/extensions/oromolang
```

Example (Linux):

```bash
ln -s /home/firaol/Documents/Projects/afaan-oromo-lang/vscode-oromolang ~/.cursor/extensions/oromolang
```

Reload Cursor. Edits under `vscode-oromolang/` in the repo apply immediately.

#### Option B — Symlink on Windows (PowerShell)

Run **PowerShell as Administrator**. Change `You` and the path to match your machine:

```powershell
New-Item -ItemType SymbolicLink -Force `
  -Path "$env:USERPROFILE\.cursor\extensions\oromolang" `
  -Target "C:\Users\You\Documents\afaan-oromo-lang\vscode-oromolang"
```

Or in **Git Bash** on Windows:

```bash
ln -s "/c/Users/You/Documents/afaan-oromo-lang/vscode-oromolang" \
  "$USERPROFILE/.cursor/extensions/oromolang"
```

Reload Cursor.


```bash
alias aoc='python3 /path/to/afaan-oromo-lang/run.py'
```

## How to run

| What | Command |
|------|---------|
| **Run** (transpile + execute) | `aoc program.ao` |
| Compile only | `ao program.ao` or `python translator.py program.ao` |
| From repo without pip | `python run.py program.ao` (Linux/macOS: `./ao program.ao`) |

Run generated Python manually: `python3 python/test.py`

> `python3 program.ao` does **not** work — use `aoc` or `run.py`.

**Save your file** (Ctrl+S) before running. An empty file on disk produces no output.

### Build output (`python/`)

| Source | Generated |
|--------|-----------|
| `test.ao` | `python/test.py` |
| `examples/hello.ao` | `python/examples/hello.py` |
| `examples/math.ao` (imported) | `python/examples/math_ao.py` |

Edit only `.ao` files; `python/` is generated output (git-ignored).

---

## Keywords (Afaan Oromoo → Python)

Defined in `src/lexer/tokens.py`. Each keyword maps automatically in generated Python.

### Core

| Afaan Oromoo | Python | Notes |
|--------------|--------|-------|
| `gocha` | `def` | function |
| `hojii` | `def` | legacy alias for `gocha` |
| `deebisi` | `return` | |
| `yoo` | `if` | |
| `yookiin` | `else` | |
| `hanga` | `while` | |
| `dhugaa` | `True` | |
| `soba` | `False` | |
| `maxxansi` | `print` | |

### Logic and operators

| Afaan Oromoo | Python |
|--------------|--------|
| `fi` | `and` |
| `yookaan` | `or` |
| `miti` | `not` |
| `keessa` | `in` |
| `dha` | `is` |

### Loops and flow

| Afaan Oromoo | Python |
|--------------|--------|
| `yookaas` | `elif` |
| `marsaa` | `for` |
| `dhaabi` | `break` |
| `fufi` | `continue` |
| `homaa` | `None` |
| `dhiisi` | `pass` |

### Error handling

| Afaan Oromoo | Python |
|--------------|--------|
| `yaali` | `try` |
| `qabi` | `except` |
| `xumura` | `finally` |
| `darbadhu` | `raise` |
| `mirkaneessi` | `assert` |

### Object-oriented

| Afaan Oromoo | Python |
|--------------|--------|
| `caasaa` | `class` |
| `haqi` | `del` |

### Imports

| Afaan Oromoo | Python | Example |
|--------------|--------|---------|
| `fidi` | `import` | `fidi math` → `import math` |
| `irraa` | `from` | `irraa math` → `from math import *` |
| `fuudhu` | `from` | `fuudhu math` → `from math import *` (legacy) |
| `akka` | `as` | |

### Scope

| Afaan Oromoo | Python |
|--------------|--------|
| `waliigalaa` | `global` |
| `ala` | `nonlocal` |

### Generators and async

| Afaan Oromoo | Python |
|--------------|--------|
| `lakkisi` | `yield` |
| `cinatti` | `async` |
| `eegi` | `await` |

### Other

| Afaan Oromoo | Python |
|--------------|--------|
| `dhokataa` | `lambda` |
| `waliin` | `with` |

---

## Syntax (short)

**Blocks** use `{` `}` (not indentation in `.ao`):

```text
yoo (x > 5) {
    maxxansi(x)
} yookaas (x == 0) {
    dhiisi
} yookiin {
    maxxansi(homaa)
}

gocha ida'uu(a, b) {
    deebisi a + b
}

marsaa (i keessa range(3)) {
    maxxansi(i)
}
```

**Operators:** `+` `-` `*` `/` `==` `<` `>`

**Import a module** (`fuudhu` / `irraa` — looks in the same folder or `lib/`):

```text
fuudhu math
maxxansi(walitti(10, 7))
```

**Examples:** `examples/hello.ao`, `examples/app.ao`, `examples/keywords.ao`

```bash
aoc examples/hello.ao
```

## Errors

Messages are in Afaan Oromoo (e.g. missing `}`, empty file, module not found). Save the file if you see an empty-file error.
