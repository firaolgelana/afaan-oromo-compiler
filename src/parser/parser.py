"""Recursive descent parser for the Afaan Oromoo language."""

from __future__ import annotations

from typing import List, Optional

from ..errors.diagnostics import DiagnosticError, Diagnostics, SourceLocation
from ..lexer.tokens import Token, TokenType
from .ast import (
    Assign,
    BinaryOp,
    Boolean,
    ExprStmt,
    Expression,
    FunctionCall,
    FunctionDef,
    Identifier,
    If,
    Import,
    Number,
    Program,
    Return,
    Statement,
    While,
)


class Parser:
    """Builds an AST from a token stream using recursive descent."""

    def __init__(self, tokens: List[Token], diagnostics: Optional[Diagnostics] = None) -> None:
        self.tokens = tokens
        self.diagnostics = diagnostics or Diagnostics()
        self.pos = 0

    @property
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1]

    def location(self) -> SourceLocation:
        return SourceLocation(self.current.line, self.current.column)

    def advance(self) -> Token:
        tok = self.current
        if self.current.type != TokenType.EOF:
            self.pos += 1
        return tok

    def match(self, *types: TokenType) -> bool:
        return self.current.type in types

    def expect(self, token_type: TokenType, error_key: str = "invalid_syntax") -> Token:
        if self.current.type == token_type:
            return self.advance()
        loc = self.location()
        if token_type == TokenType.RBRACE:
            self.diagnostics.raise_error("missing_rbrace", loc)
        elif token_type == TokenType.LBRACE:
            self.diagnostics.raise_error("missing_lbrace", loc)
        elif token_type == TokenType.RPAREN:
            self.diagnostics.raise_error("missing_rparen", loc)
        elif token_type == TokenType.LPAREN:
            self.diagnostics.raise_error("missing_lparen", loc)
        else:
            self.diagnostics.raise_error(
                "unexpected_token",
                loc,
                token=self.current.type.name,
            )
        raise DiagnosticError(self.diagnostics.MESSAGES[error_key], loc)

    def parse(self) -> Program:
        statements: List[Statement] = []
        try:
            while not self.match(TokenType.EOF):
                statements.append(self.parse_statement())
            return Program(statements=statements)
        except DiagnosticError:
            raise

    def parse_statement(self) -> Statement:
        if self.match(TokenType.FUUDHU):
            return self.parse_import()
        if self.match(TokenType.HOJII):
            return self.parse_function_def()
        if self.match(TokenType.YOO):
            return self.parse_if()
        if self.match(TokenType.HANGA):
            return self.parse_while()
        if self.match(TokenType.DEEBISI):
            return self.parse_return()
        if self.match(TokenType.IDENTIFIER) and self.peek(1).type == TokenType.EQ:
            return self.parse_assignment()
        if self.match(TokenType.MAXXANSI):
            return self.parse_print_stmt()
        if self.match(TokenType.IDENTIFIER) and self.peek(1).type == TokenType.LPAREN:
            return ExprStmt(expression=self.parse_function_call())

        self.diagnostics.raise_error("invalid_syntax", self.location())
        raise DiagnosticError(self.diagnostics.MESSAGES["invalid_syntax"], self.location())

    def parse_import(self) -> Import:
        self.advance()  # fuudhu
        if self.match(TokenType.STRING):
            return Import(module=self.advance().value)
        if self.match(TokenType.IDENTIFIER):
            return Import(module=self.advance().value)
        self.diagnostics.raise_error("invalid_syntax", self.location())
        raise DiagnosticError(self.diagnostics.MESSAGES["invalid_syntax"], self.location())

    def parse_block(self) -> List[Statement]:
        self.expect(TokenType.LBRACE)
        body: List[Statement] = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            body.append(self.parse_statement())
        if self.match(TokenType.EOF):
            self.diagnostics.raise_error("missing_rbrace", self.location())
            raise DiagnosticError(self.diagnostics.MESSAGES["missing_rbrace"], self.location())
        self.expect(TokenType.RBRACE)
        return body

    def parse_assignment(self) -> Assign:
        name_tok = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.EQ)
        value = self.parse_expression()
        return Assign(name=name_tok.value, value=value)

    def parse_if(self) -> If:
        self.advance()  # yoo
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_body = self.parse_block()
        else_body: Optional[List[Statement]] = None
        if self.match(TokenType.YOOKIIN):
            self.advance()
            else_body = self.parse_block()
        return If(condition=condition, then_body=then_body, else_body=else_body)

    def parse_while(self) -> While:
        self.advance()  # hanga
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return While(condition=condition, body=body)

    def parse_function_def(self) -> FunctionDef:
        self.advance()  # hojii
        name_tok = self.expect(TokenType.IDENTIFIER, "expected_identifier")
        self.expect(TokenType.LPAREN)
        params: List[str] = []
        if not self.match(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return FunctionDef(name=name_tok.value, params=params, body=body)

    def parse_return(self) -> Return:
        self.advance()  # deebisi
        value = self.parse_expression()
        return Return(value=value)

    def parse_print_stmt(self) -> ExprStmt:
        call = self.parse_maxxansi_call()
        return ExprStmt(expression=call)

    def parse_maxxansi_call(self) -> FunctionCall:
        self.advance()  # maxxansi
        self.expect(TokenType.LPAREN)
        args: List[Expression] = []
        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.parse_expression())
        self.expect(TokenType.RPAREN)
        return FunctionCall(name="maxxansi", args=args)

    def parse_function_call(self) -> FunctionCall:
        name_tok = self.advance()
        self.expect(TokenType.LPAREN)
        args: List[Expression] = []
        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.parse_expression())
        self.expect(TokenType.RPAREN)
        return FunctionCall(name=name_tok.value, args=args)

    def parse_expression(self) -> Expression:
        return self.parse_comparison()

    def parse_comparison(self) -> Expression:
        left = self.parse_additive()
        while self.match(TokenType.EQEQ, TokenType.LT, TokenType.GT):
            op_tok = self.advance()
            right = self.parse_additive()
            left = BinaryOp(left=left, op=op_tok.value, right=right)
        return left

    def parse_additive(self) -> Expression:
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_tok = self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left=left, op=op_tok.value, right=right)
        return left

    def parse_multiplicative(self) -> Expression:
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op_tok = self.advance()
            right = self.parse_unary()
            left = BinaryOp(left=left, op=op_tok.value, right=right)
        return left

    def parse_unary(self) -> Expression:
        if self.match(TokenType.MINUS):
            self.advance()
            operand = self.parse_unary()
            return BinaryOp(left=Number(0), op="-", right=operand)
        return self.parse_primary()

    def parse_primary(self) -> Expression:
        if self.match(TokenType.NUMBER):
            tok = self.advance()
            return Number(value=tok.value)
        if self.match(TokenType.DHUGAA):
            self.advance()
            return Boolean(value=True)
        if self.match(TokenType.SOBA):
            self.advance()
            return Boolean(value=False)
        if self.match(TokenType.MAXXANSI):
            return self.parse_maxxansi_call()
        if self.match(TokenType.IDENTIFIER):
            if self.peek(1).type == TokenType.LPAREN:
                return self.parse_function_call()
            tok = self.advance()
            return Identifier(name=tok.value)
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr

        self.diagnostics.raise_error("expected_expression", self.location())
        raise DiagnosticError(self.diagnostics.MESSAGES["expected_expression"], self.location())
