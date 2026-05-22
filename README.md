# Afaan Oromoo Language → Python Transpiler

A beginner-friendly programming language with **Afaan Oromoo** keywords, transpiled to **Python 3** through a real compiler pipeline:

```
.ao source  →  Lexer  →  Parser (AST)  →  Code Generator  →  .py  →  Python
```

No regex substitution — the implementation uses a traditional lexer, recursive-descent parser, and AST visitor.

## Requirements

- Python 3.10 or newer

## Quick start

### 1. Create a program

Save a file named `test.ao` (extension **`.ao`**, not `.io`):

```text
maxxansi(10)
maxxansi(5)
```

**Important:** Save the file (**Ctrl+S** / **Cmd+S**) before running. If the file is empty on disk, nothing will print.

### 2. Run it (recommended — one step)

From the project folder:

```bash
python3 run.py test.ao
```

This transpiles `test.ao` → `python/test.py` and runs it automatically (your `.ao` source stays in place; generated Python lives under `python/`, like TypeScript’s `outDir`). Expected output:

```text
10
5
```

### 3. Or compile and run separately

```bash
# Compile only (creates python/test.py)
python3 translator.py test.ao

# Run the generated Python yourself
python3 python/test.py
```

## Commands

| Goal | Command |
|------|---------|
| **Run** (transpile + execute) | `python3 run.py program.ao` |
| **Compile only** | `python3 translator.py program.ao` |
| **Compile and run** | `python3 translator.py program.ao --run` |
| **Shell shortcut** | `./ao program.ao` |
| **Alias (like `tsc`)** | `alias aoc='python3 /path/to/afaan-oromo-lang/run.py'` then `aoc test.ao` |

> **Note:** `python3 program.ao` does **not** work — Python cannot read `.ao` syntax directly. Always use `run.py`, `translator.py --run`, or `./ao`.

### Output folder (`python/`)

All transpiled `.py` files go under **`python/`** at the project root (configured in `pythoncompiler/`). Example:

| Source | Generated |
|--------|-----------|
| `test.ao` | `python/test.py` |
| `examples/hello.ao` | `python/examples/hello.py` |
| `examples/math.ao` (imported) | `python/examples/math_ao.py` |

You only edit `.ao` files; `python/` is build output (ignored by git).

## Keywords (Afaan Oromoo → Python)

| Afaan Oromoo | Meaning | Python |
|--------------|---------|--------|
| `hojii` | function | `def` |
| `deebisi` | return | `return` |
| `yoo` | if | `if` |
| `yookiin` | else | `else` |
| `hanga` | while | `while` |
| `dhugaa` | true | `True` |
| `soba` | false | `False` |
| `maxxansi` | print | `print` |
| `fuudhu` | import library | `from … import *` |

## Syntax

### Variables and math

```text
x = 10
y = x + 5 * 2
```

Operators: `+`, `-`, `*`, `/`, `==`, `<`, `>`

### Blocks use `{` `}` (required)

Indentation in `.ao` is optional; the transpiler emits correct Python indentation.

```text
yoo (x > 5) {
    maxxansi(x)
} yookiin {
    maxxansi(0)
}

hanga (x < 10) {
    x = x + 1
}
```

Semicolons (`;`) are **not** used.

### Functions

```text
hojii ida'uu(a, b) {
    deebisi a + b
}

maxxansi(ida'uu(3, 4))
```

Apostrophes in names (e.g. `ida'uu`) are mapped to underscores in Python (`ida_uu`).

### Import a library (`fuudhu`)

**`examples/math.ao`** — library:

```text
hojii walitti(a, b) {
    deebisi a + b
}
```

**`examples/app.ao`** — main program:

```text
fuudhu math
maxxansi(walitti(10, 7))
```

Also:

```text
fuudhu "math.ao"
```

The compiler looks for the file in:

1. The same folder as the importing `.ao` file
2. A `lib/` subfolder

Generated files (under `python/`):

- Main program: `app.ao` → `python/examples/app.py`
- Library: `math.ao` → `python/examples/math_ao.py` (the `_ao` suffix avoids clashing with Python’s built-in `math` module)

Run the example:

```bash
python3 run.py examples/app.ao
```

## Project structure

```
afaan-oromo-lang/
├── README.md
├── translator.py        # CLI: compile / --run
├── run.py               # CLI: compile + run (shortcut)
├── ao                   # Shell wrapper for run.py
├── pyproject.toml
├── pythoncompiler/      # Output paths (python/ outDir)
├── python/              # Generated .py (build output)
├── src/
│   ├── lexer/           # Tokenizer
│   ├── parser/          # AST + recursive descent parser
│   ├── codegen/         # Python code generator
│   ├── compiler/        # Multi-file / import handling
│   ├── errors/          # Afaan Oromoo error messages
│   └── utils/
└── examples/
    ├── hello.ao
    ├── app.ao
    └── math.ao
```

## Error messages

Errors are reported in **Afaan Oromoo**, for example:

| Situation | Message |
|-----------|---------|
| Missing `}` | `Dogoggora: Mallattoo '}' irraanfatteerta.` |
| Invalid syntax | `Dogoggora: Caasaa himaa sirrii miti.` |
| Empty file | `Dogoggora: Faayiliin duwwaa dha. Barruu .ao kee barreessi (Save: Ctrl+S).` |
| Module not found | `Dogoggora: Faayilii galmee '…' hin argamne.` |

## Optional: shell alias or install

**Alias** (run any `.ao` file; output goes to `python/`):

```bash
alias aoc='python3 /full/path/to/afaan-oromo-lang/run.py'
aoc test.ao
```

**Install** the `ao` command:

```bash
pip install -e .
ao test.ao
```

## Troubleshooting

**Ran `python3 run.py test.ao` but nothing printed**

1. Save `test.ao` in your editor (**Ctrl+S**).
2. Confirm on disk: `cat test.ao` should show your code.
3. Check `python/test.py` — it should contain lines like `print(10)`.

**`python3 test.ao` fails**

Use `python3 run.py test.ao` instead. The `.ao` file must be transpiled first (or use `run.py`, which does both steps).

## Example: full program

See `examples/hello.ao` for variables, `yoo` / `yookiin`, `hanga`, and functions.

```bash
python3 run.py examples/hello.ao
```