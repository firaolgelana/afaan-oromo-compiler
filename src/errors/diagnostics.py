"""Localized error reporting in Afaan Oromoo."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class SourceLocation:
    line: int
    column: int


class DiagnosticError(Exception):
    """Raised when lexing or parsing fails."""

    def __init__(self, message: str, location: Optional[SourceLocation] = None) -> None:
        self.message = message
        self.location = location
        super().__init__(message)


class Diagnostics:
    """Collects and prints friendly Afaan Oromoo error messages."""

    MESSAGES = {
        "missing_rbrace": "Dogoggora: Mallattoo '}}' irraanfatteerta.",
        "missing_lbrace": "Dogoggora: Mallattoo '{{' irraanfatteerta.",
        "missing_rparen": "Dogoggora: Mallattoo ')' irraanfatteerta.",
        "missing_lparen": "Dogoggora: Mallattoo '(' irraanfatteerta.",
        "invalid_syntax": "Dogoggora: Caasaa himaa sirrii miti.",
        "unexpected_token": "Dogoggora: Mallattoo hin eegamne: {token}.",
        "unexpected_eof": "Dogoggora: Barruun xumurrame.",
        "invalid_character": "Dogoggora: Arfiin hin beekamne: {char}.",
        "expected_identifier": "Dogoggora: Maqaa barbaachisa.",
        "expected_expression": "Dogoggora: Himannoo barbaachisa.",
        "module_not_found": "Dogoggora: Faayilii galmee '{name}' hin argamne.",
        "circular_import": "Dogoggora: Fuudhuwwan naanna'aa (circular import).",
    }

    def __init__(self, source: str = "") -> None:
        self.source = source
        self._errors: list[str] = []

    def format_location(self, location: Optional[SourceLocation]) -> str:
        if location is None:
            return ""
        return f" (giddugaleessa {location.line}:{location.column})"

    def _format_message(self, key: str, **kwargs: str) -> str:
        template = self.MESSAGES.get(key, self.MESSAGES["invalid_syntax"])
        if kwargs:
            return template.format(**kwargs)
        return template.format()

    def report(self, key: str, location: Optional[SourceLocation] = None, **kwargs: str) -> None:
        message = self._format_message(key, **kwargs)
        loc_suffix = self.format_location(location)
        full = f"{message}{loc_suffix}"
        self._errors.append(full)

    def report_custom(self, message: str, location: Optional[SourceLocation] = None) -> None:
        loc_suffix = self.format_location(location)
        self._errors.append(f"{message}{loc_suffix}")

    def raise_error(self, key: str, location: Optional[SourceLocation] = None, **kwargs: str) -> None:
        message = self._format_message(key, **kwargs)
        raise DiagnosticError(message, location)

    def emit_and_exit(self) -> None:
        for err in self._errors:
            print(err, file=sys.stderr)
        if self._errors:
            sys.exit(1)

    def has_errors(self) -> bool:
        return len(self._errors) > 0
