"""Multi-file transpilation: imports, dependency order, output .py files."""

from __future__ import annotations

from pathlib import Path
from typing import List, Set

from ..codegen.python_generator import PythonGenerator
from ..errors.diagnostics import Diagnostics, SourceLocation
from ..lexer.lexer import Lexer, strip_shebang
from ..parser.ast import Import, Program
from ..parser.parser import Parser
from pythoncompiler.paths import find_project_root

from ..utils.file_io import output_path_for, read_source, write_output
from ..utils.modules import normalize_import_spec, resolve_module_path


class ProjectCompiler:
    """Transpile an entry .ao file and all fuudhu (import) dependencies."""

    def __init__(self) -> None:
        self._compiled: Set[Path] = set()
        self._project_root: Path | None = None

    def compile_entry(self, entry: Path) -> Path:
        """Transpile entry and dependencies. Returns path to generated main .py."""
        self._compiled.clear()
        entry = entry.resolve()
        self._project_root = find_project_root(entry)
        self._compile_recursive(entry, [], is_entry=True)
        return output_path_for(entry, project_root=self._project_root, is_entry=True)

    def _compile_recursive(
        self, source_path: Path, stack: List[Path], *, is_entry: bool
    ) -> None:
        path = source_path.resolve()
        if path in stack:
            Diagnostics().raise_error("circular_import", SourceLocation(1, 1))
        if path in self._compiled:
            return

        stack = stack + [path]
        program = self._parse_file(path)

        for stmt in program.statements:
            if isinstance(stmt, Import):
                try:
                    dep = resolve_module_path(path, stmt.module)
                except FileNotFoundError:
                    Diagnostics().raise_error(
                        "module_not_found",
                        None,
                        name=normalize_import_spec(stmt.module),
                    )
                if dep is not None:
                    self._compile_recursive(dep, stack, is_entry=False)

        generator = PythonGenerator()
        out = output_path_for(
            path, project_root=self._project_root, is_entry=is_entry
        )
        write_output(out, generator.generate(program))
        self._compiled.add(path)

    def _parse_file(self, path: Path) -> Program:
        raw = read_source(path)
        source = strip_shebang(raw)
        diagnostics = Diagnostics(source)
        lexer = Lexer(source, diagnostics)
        tokens = lexer.tokenize()
        parser = Parser(tokens, diagnostics)
        return parser.parse()
