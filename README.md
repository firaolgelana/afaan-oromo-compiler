# Afaan Oromoo → Python

Write programs in **Afaan Oromoo** (`.ao` files); the transpiler compiles them to Python under `python/` and runs them.

```
.ao  →  Lexer  →  Parser  →  Code Generator  →  python/*.py  →  Python
```

**Requirements:** Python 3.10+

## How to run

### 1. Set up the `aoc` alias (recommended)

Add to `~/.bashrc` or `~/.zshrc` (use your real project path):

```bash
alias aoc='python3 /home/firaol/Documents/Projects/afaan-oromo-lang/run.py'
```

Reload the shell, then run any `.ao` file from anywhere:

```bash
aoc test.ao
aoc examples/hello.ao
```

`aoc` transpiles to `python/` and executes the result in one step (like TypeScript compile + run).

### 2. Other ways

| What | Command |
|------|---------|
| Run (transpile + execute) | `python3 run.py program.ao` |
| Compile only | `python3 translator.py program.ao` |
| Compile and run | `python3 translator.py program.ao --run` |
| Shell script | `./ao program.ao` |
| Installed CLI | `pip install -e .` then `ao program.ao` |

Run generated Python manually: `python3 python/test.py`

> `python3 program.ao` does **not** work — use `aoc`, `run.py`, or `./ao`.

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
