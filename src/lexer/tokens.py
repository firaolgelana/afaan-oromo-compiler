"""Token definitions and Afaan Oromoo → Python keyword mapping."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    """Token kinds; keyword types align with their Python equivalent."""

    # Core
    DEF = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    TRUE = auto()
    FALSE = auto()

    # Logic & operators (also used as expression keywords)
    AND = auto()
    OR = auto()
    NOT = auto()
    IN = auto()
    IS = auto()

    # Loops & flow
    ELIF = auto()
    FOR = auto()
    BREAK = auto()
    CONTINUE = auto()
    NONE = auto()
    PASS = auto()

    # Errors
    TRY = auto()
    EXCEPT = auto()
    FINALLY = auto()
    RAISE = auto()
    ASSERT = auto()

    # OOP & builtins
    CLASS = auto()
    DEL = auto()

    # Imports
    IMPORT = auto()
    FROM = auto()
    AS = auto()
    IMPORT_LIB = auto()  # fuudhu: from <module> import *

    # Scope
    GLOBAL = auto()
    NONLOCAL = auto()

    # Async & generators
    YIELD = auto()
    ASYNC = auto()
    AWAIT = auto()

    # Misc
    LAMBDA = auto()
    WITH = auto()
    PRINT = auto()  # maxxansi → print

    # Literals & identifiers
    STRING = auto()
    IDENTIFIER = auto()
    NUMBER = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    STARSTAR = auto()
    SLASH = auto()
    SLASHSLASH = auto()
    EQ = auto()
    EQEQ = auto()
    LT = auto()
    GT = auto()
    BANGEQ = auto()
    LTE = auto()
    GTE = auto()
    MOD = auto()
    PLUSEQ = auto()
    MINUSEQ = auto()
    PLUSPLUS = auto()
    MINUSMINUS = auto()

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    DOT = auto()
    COLON = auto()
    COMMA = auto()

    # Structural
    NEWLINE = auto()
    EOF = auto()


# Afaan Oromoo spelling → (token type, Python keyword)
# Legacy spellings (hojii, fuudhu, maxxansi) kept for existing .ao files.
KEYWORD_SPECS: dict[str, tuple[TokenType, str]] = {
    # 1. Core
    "gocha": (TokenType.DEF, "def"),
    "hojii": (TokenType.DEF, "def"),
    "deebisi": (TokenType.RETURN, "return"),
    "yoo": (TokenType.IF, "if"),
    "yookiin": (TokenType.ELSE, "else"),
    "hanga": (TokenType.WHILE, "while"),
    "dhugaa": (TokenType.TRUE, "True"),
    "soba": (TokenType.FALSE, "False"),
    # 2. Logic & operators
    "fi": (TokenType.AND, "and"),
    "yookaan": (TokenType.OR, "or"),
    "miti": (TokenType.NOT, "not"),
    "keessa": (TokenType.IN, "in"),
    "dha": (TokenType.IS, "is"),
    # 3. Loops & flow
    "yookaas": (TokenType.ELIF, "elif"),
    "marsaa": (TokenType.FOR, "for"),
    "dhaabi": (TokenType.BREAK, "break"),
    "fufi": (TokenType.CONTINUE, "continue"),
    "homaa": (TokenType.NONE, "None"),
    "dhiisi": (TokenType.PASS, "pass"),
    # 4. Error handling
    "yaali": (TokenType.TRY, "try"),
    "qabi": (TokenType.EXCEPT, "except"),
    "xumura": (TokenType.FINALLY, "finally"),
    "darbadhu": (TokenType.RAISE, "raise"),
    "mirkaneessi": (TokenType.ASSERT, "assert"),
    # 5. OOP
    "caasaa": (TokenType.CLASS, "class"),
    "haqi": (TokenType.DEL, "del"),
    # 6. Imports
    "fidi": (TokenType.IMPORT, "import"),
    "irraa": (TokenType.FROM, "from"),
    "fuudhu": (TokenType.IMPORT_LIB, "from"),
    "akka": (TokenType.AS, "as"),
    # 7. Scope
    "waliigalaa": (TokenType.GLOBAL, "global"),
    "ala": (TokenType.NONLOCAL, "nonlocal"),
    # 8. Generators & async
    "lakkisi": (TokenType.YIELD, "yield"),
    "cinatti": (TokenType.ASYNC, "async"),
    "eegi": (TokenType.AWAIT, "await"),
    # 9. Misc
    "dhokataa": (TokenType.LAMBDA, "lambda"),
    "waliin": (TokenType.WITH, "with"),
    "maxxansi": (TokenType.PRINT, "print"),
}

# Quick lookup: spelling → token type (for lexer)
KEYWORDS: dict[str, TokenType] = {k: v[0] for k, v in KEYWORD_SPECS.items()}

# Token type → Python keyword (for codegen)
PYTHON_KEYWORD: dict[TokenType, str] = {
    t: py for t, py in {v[0]: v[1] for v in KEYWORD_SPECS.values()}.items()
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


def python_keyword_for(token_type: TokenType) -> Optional[str]:
    return PYTHON_KEYWORD.get(token_type)


def python_keyword_for_word(word: str) -> Optional[str]:
    spec = KEYWORD_SPECS.get(word)
    return spec[1] if spec else None
