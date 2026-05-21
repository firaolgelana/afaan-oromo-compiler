"""Token definitions for the Afaan Oromoo source language."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    # Keywords (Afaan Oromoo)
    HOJII = auto()       # function def
    DEEBISI = auto()     # return
    YOO = auto()         # if
    YOOKIIN = auto()     # else
    HANGA = auto()       # while
    DHUGAA = auto()      # True
    SOBA = auto()        # False
    MAXXANSI = auto()    # print
    FUUDHU = auto()      # import (library)

    # Literals & identifiers
    STRING = auto()
    IDENTIFIER = auto()
    NUMBER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQ = auto()          # =
    EQEQ = auto()        # ==
    LT = auto()
    GT = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()

    # Structural
    NEWLINE = auto()
    EOF = auto()


# Map keyword spellings to token types
KEYWORDS: dict[str, TokenType] = {
    "hojii": TokenType.HOJII,
    "deebisi": TokenType.DEEBISI,
    "yoo": TokenType.YOO,
    "yookiin": TokenType.YOOKIIN,
    "hanga": TokenType.HANGA,
    "dhugaa": TokenType.DHUGAA,
    "soba": TokenType.SOBA,
    "maxxansi": TokenType.MAXXANSI,
    "fuudhu": TokenType.FUUDHU,
}


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"


def keyword_token_type(word: str) -> Optional[TokenType]:
    return KEYWORDS.get(word)
