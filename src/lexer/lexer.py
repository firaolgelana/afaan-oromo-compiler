"""String-scanning lexer with Unicode identifier support."""

from __future__ import annotations

from typing import Iterator, Optional

from ..errors.diagnostics import DiagnosticError, Diagnostics, SourceLocation
from .tokens import KEYWORDS, Token, TokenType, keyword_token_type


def strip_shebang(source: str) -> str:
    """Remove #! line so .ao files can be executable scripts."""
    if source.startswith("#!"):
        newline = source.find("\n")
        if newline == -1:
            return ""
        return source[newline + 1 :]
    return source


class Lexer:
    """Tokenizes Afaan Oromoo source text character by character."""

    def __init__(self, source: str, diagnostics: Optional[Diagnostics] = None) -> None:
        self.source = source
        self.diagnostics = diagnostics or Diagnostics(source)
        self.pos = 0
        self.line = 1
        self.column = 1
        self._tokens: list[Token] = []

    @property
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]

    def advance(self) -> Optional[str]:
        ch = self.current_char
        if ch is None:
            return None
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def peek(self, offset: int = 0) -> Optional[str]:
        idx = self.pos + offset
        if idx >= len(self.source):
            return None
        return self.source[idx]

    def location(self) -> SourceLocation:
        return SourceLocation(self.line, self.column)

    def skip_whitespace_and_comments(self) -> None:
        while self.current_char is not None:
            if self.current_char in " \t\r":
                self.advance()
            elif self.current_char == "\n":
                self.advance()
            elif self.current_char == "#":
                while self.current_char is not None and self.current_char != "\n":
                    self.advance()
            else:
                break

    def read_number(self, start_line: int, start_col: int) -> Token:
        num_str = ""
        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):
            if self.current_char == "." and "." in num_str:
                break
            num_str += self.advance()
        if "." in num_str:
            value: int | float = float(num_str)
        else:
            value = int(num_str)
        return Token(TokenType.NUMBER, value, start_line, start_col)

    def is_identifier_start(self, ch: str) -> bool:
        return ch.isalpha() or ch == "_" or ch == "'"

    def is_identifier_part(self, ch: str) -> bool:
        return ch.isalnum() or ch in "_'"

    def read_identifier_or_keyword(self, start_line: int, start_col: int) -> Token:
        ident = ""
        while self.current_char is not None and self.is_identifier_part(self.current_char):
            ident += self.advance()
        kw = keyword_token_type(ident)
        if kw is not None:
            return Token(kw, ident, start_line, start_col)
        return Token(TokenType.IDENTIFIER, ident, start_line, start_col)

    def read_string(self, start_line: int, start_col: int) -> Token:
        quote = self.advance()
        is_triple = False
        if self.current_char == quote and self.peek(1) == quote:
            is_triple = True
            self.advance()
            self.advance()
            
        value = ""
        closed = False
        while self.current_char is not None:
            if is_triple:
                if self.current_char == quote and self.peek(1) == quote and self.peek(2) == quote:
                    self.advance()
                    self.advance()
                    self.advance()
                    closed = True
                    break
            else:
                if self.current_char == quote:
                    self.advance()
                    closed = True
                    break
            
            if self.current_char == "\\":
                self.advance()
                esc = self.current_char
                if esc is None:
                    break
                value += self.advance() or ""
            else:
                value += self.advance()
                
        if not closed:
            self.diagnostics.raise_error("invalid_syntax", self.location())
            
        return Token(TokenType.STRING, value, start_line, start_col)

    def tokenize(self) -> list[Token]:
        self._tokens = []
        try:
            while self.current_char is not None:
                self.skip_whitespace_and_comments()
                if self.current_char is None:
                    break

                start_line, start_col = self.line, self.column
                ch = self.current_char

                if ch.isdigit():
                    self._tokens.append(self.read_number(start_line, start_col))
                    continue

                if self.is_identifier_start(ch):
                    self._tokens.append(self.read_identifier_or_keyword(start_line, start_col))
                    continue

                if ch == '"':
                    self._tokens.append(self.read_string(start_line, start_col))
                    continue

                two = ch + (self.peek(1) or "")
                two_map = {
                    "==": TokenType.EQEQ,
                    "!=": TokenType.BANGEQ,
                    "<=": TokenType.LTE,
                    ">=": TokenType.GTE,
                    "+=": TokenType.PLUSEQ,
                    "-=": TokenType.MINUSEQ,
                    "++": TokenType.PLUSPLUS,
                    "--": TokenType.MINUSMINUS,
                    "**": TokenType.STARSTAR,
                    "//": TokenType.SLASHSLASH,
                }
                if two in two_map:
                    self.advance()
                    self.advance()
                    self._tokens.append(Token(two_map[two], two, start_line, start_col))
                    continue

                single_map = {
                    "+": TokenType.PLUS,
                    "-": TokenType.MINUS,
                    "*": TokenType.STAR,
                    "/": TokenType.SLASH,
                    "%": TokenType.MOD,
                    "=": TokenType.EQ,
                    "<": TokenType.LT,
                    ">": TokenType.GT,
                    "(": TokenType.LPAREN,
                    ")": TokenType.RPAREN,
                    "{": TokenType.LBRACE,
                    "}": TokenType.RBRACE,
                    "[": TokenType.LBRACKET,
                    "]": TokenType.RBRACKET,
                    ".": TokenType.DOT,
                    ":": TokenType.COLON,
                    ",": TokenType.COMMA,
                }
                if ch in single_map:
                    self.advance()
                    self._tokens.append(Token(single_map[ch], ch, start_line, start_col))
                    continue

                self.diagnostics.raise_error(
                    "invalid_character",
                    self.location(),
                    char=repr(ch),
                )

            self._tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        except DiagnosticError:
            raise
        return self._tokens

    def __iter__(self) -> Iterator[Token]:
        if not self._tokens:
            self.tokenize()
        return iter(self._tokens)
