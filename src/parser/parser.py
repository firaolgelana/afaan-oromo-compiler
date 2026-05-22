"""Recursive descent parser for the Afaan Oromoo language."""

from __future__ import annotations

from typing import List, Optional

from ..errors.diagnostics import DiagnosticError, Diagnostics, SourceLocation
from ..lexer.tokens import Token, TokenType
from .ast import (
    Assert,
    Assign,
    Await,
    BinaryOp,
    Boolean,
    Break,
    ClassDef,
    Continue,
    Del,
    ElifBranch,
    ExceptHandler,
    ExprStmt,
    Expression,
    ForLoop,
    Call,
    FunctionDef,
    GlobalStmt,
    Identifier,
    If,
    Import,
    NoneLiteral,
    NonlocalStmt,
    Number,
    Pass,
    Program,
    Raise,
    Return,
    Statement,
    TryStmt,
    UnaryOp,
    While,
    With,
    Yield,
    StringLiteral,
    Subscript,
    Attribute,
    Dictionary,
    ListLiteral,
    AugAssign,
    IncDecStmt,
    TupleLiteral,
    SetLiteral,
    ListComprehension,
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
        if self.match(TokenType.IMPORT_LIB, TokenType.FROM):
            return self.parse_import_from_star()
        if self.match(TokenType.IMPORT):
            return self.parse_import_module()
        if self.match(TokenType.ASYNC):
            return self.parse_async_function_def()
        if self.match(TokenType.DEF):
            return self.parse_function_def()
        if self.match(TokenType.CLASS):
            return self.parse_class_def()
        if self.match(TokenType.IF):
            return self.parse_if()
        if self.match(TokenType.WHILE):
            return self.parse_while()
        if self.match(TokenType.FOR):
            return self.parse_for()
        if self.match(TokenType.TRY):
            return self.parse_try()
        if self.match(TokenType.RETURN):
            return self.parse_return()
        if self.match(TokenType.YIELD):
            return self.parse_yield_stmt()
        if self.match(TokenType.RAISE):
            return self.parse_raise()
        if self.match(TokenType.ASSERT):
            return self.parse_assert()
        if self.match(TokenType.DEL):
            return self.parse_del()
        if self.match(TokenType.GLOBAL):
            return self.parse_global()
        if self.match(TokenType.NONLOCAL):
            return self.parse_nonlocal()
        if self.match(TokenType.BREAK):
            self.advance()
            return Break()
        if self.match(TokenType.CONTINUE):
            self.advance()
            return Continue()
        if self.match(TokenType.PASS):
            self.advance()
            return Pass()
        if self.match(TokenType.WITH):
            return self.parse_with()
        if self.match(TokenType.PRINT):
            return ExprStmt(expression=self.parse_print_call())

        # Prefix increment/decrement
        if self.match(TokenType.PLUSPLUS, TokenType.MINUSMINUS):
            op_tok = self.advance()
            target = self.parse_postfix()
            return IncDecStmt(target=target, op=op_tok.value, is_postfix=False)

        expr = self.parse_expression()

        # Postfix increment/decrement
        if self.match(TokenType.PLUSPLUS, TokenType.MINUSMINUS):
            op_tok = self.advance()
            return IncDecStmt(target=expr, op=op_tok.value, is_postfix=True)

        if self.match(TokenType.EQ):
            self.advance()
            value = self.parse_expression()
            return Assign(target=expr, value=value)

        if self.match(TokenType.PLUSEQ, TokenType.MINUSEQ):
            op_tok = self.advance()
            value = self.parse_expression()
            return AugAssign(target=expr, op=op_tok.value, value=value)

        return ExprStmt(expression=expr)

    def parse_import_from_star(self) -> Import:
        self.advance()  # fuudhu or irraa
        module = self._read_module_name()
        return Import(module=module, kind="from_star")

    def parse_import_module(self) -> Import:
        self.advance()  # fidi
        module = self._read_module_name()
        return Import(module=module, kind="import")

    def _read_module_name(self) -> str:
        if self.match(TokenType.STRING):
            return self.advance().value
        if self.match(TokenType.IDENTIFIER):
            return self.advance().value
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

    def parse_if(self) -> If:
        self.advance()  # yoo
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_body = self.parse_block()
        elif_branches: List[ElifBranch] = []
        while self.match(TokenType.ELIF):
            self.advance()
            self.expect(TokenType.LPAREN)
            elif_cond = self.parse_expression()
            self.expect(TokenType.RPAREN)
            elif_branches.append(ElifBranch(condition=elif_cond, body=self.parse_block()))
        else_body: Optional[List[Statement]] = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_body = self.parse_block()
        return If(
            condition=condition,
            then_body=then_body,
            elif_branches=elif_branches,
            else_body=else_body,
        )

    def parse_while(self) -> While:
        self.advance()
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return While(condition=condition, body=self.parse_block())

    def parse_for(self) -> ForLoop:
        self.advance()  # marsaa
        self.expect(TokenType.LPAREN)
        target_tok = self.expect(TokenType.IDENTIFIER)
        if not self.match(TokenType.IN):
            self.diagnostics.raise_error("invalid_syntax", self.location())
        self.advance()
        iterable = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return ForLoop(
            target=target_tok.value,
            iterable=iterable,
            body=self.parse_block(),
        )

    def parse_try(self) -> TryStmt:
        self.advance()  # yaali
        body = self.parse_block()
        handlers: List[ExceptHandler] = []
        while self.match(TokenType.EXCEPT):
            self.advance()
            exc_type: Optional[str] = None
            if self.match(TokenType.LPAREN):
                self.advance()
                if self.match(TokenType.IDENTIFIER):
                    exc_type = self.advance().value
                self.expect(TokenType.RPAREN)
            handlers.append(ExceptHandler(exc_type=exc_type, body=self.parse_block()))
        finally_body: Optional[List[Statement]] = None
        if self.match(TokenType.FINALLY):
            self.advance()
            finally_body = self.parse_block()
        return TryStmt(body=body, handlers=handlers, finally_body=finally_body)

    def parse_function_def(self, *, is_async: bool = False) -> FunctionDef:
        self.advance()  # gocha / hojii
        name_tok = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LPAREN)
        params: List[str] = []
        if not self.match(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        return FunctionDef(
            name=name_tok.value,
            params=params,
            body=self.parse_block(),
            is_async=is_async,
        )

    def parse_async_function_def(self) -> FunctionDef:
        self.advance()  # cinatti
        if not self.match(TokenType.DEF):
            self.diagnostics.raise_error("invalid_syntax", self.location())
        return self.parse_function_def(is_async=True)

    def parse_class_def(self) -> ClassDef:
        self.advance()  # caasaa
        name_tok = self.expect(TokenType.IDENTIFIER)
        base_class = None
        if self.match(TokenType.LPAREN):
            self.advance()
            base_class = self.parse_expression()
            self.expect(TokenType.RPAREN)
        return ClassDef(name=name_tok.value, body=self.parse_block(), base_class=base_class)

    def parse_return(self) -> Return:
        self.advance()
        if self.match(TokenType.RBRACE):
            return Return(value=None)
        return Return(value=self.parse_expression())

    def parse_yield_stmt(self) -> Yield:
        self.advance()
        if self.match(TokenType.RBRACE):
            return Yield(value=None)
        return Yield(value=self.parse_expression())

    def parse_raise(self) -> Raise:
        self.advance()
        if self.match(TokenType.RBRACE):
            return Raise(expression=None)
        return Raise(expression=self.parse_expression())

    def parse_assert(self) -> Assert:
        self.advance()
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return Assert(condition=condition)

    def parse_del(self) -> Del:
        self.advance()
        return Del(target=self.parse_expression())

    def parse_global(self) -> GlobalStmt:
        self.advance()
        names = [self.expect(TokenType.IDENTIFIER).value]
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER).value)
        return GlobalStmt(names=names)

    def parse_nonlocal(self) -> NonlocalStmt:
        self.advance()
        names = [self.expect(TokenType.IDENTIFIER).value]
        while self.match(TokenType.COMMA):
            self.advance()
            names.append(self.expect(TokenType.IDENTIFIER).value)
        return NonlocalStmt(names=names)

    def parse_with(self) -> With:
        self.advance()  # waliin
        self.expect(TokenType.LPAREN)
        context = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return With(context=context, body=self.parse_block())

    def parse_print_call(self) -> Call:
        self.advance()
        self.expect(TokenType.LPAREN)
        args: List[Expression] = []
        if not self.match(TokenType.RPAREN):
            args.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                args.append(self.parse_expression())
        self.expect(TokenType.RPAREN)
        return Call(func=Identifier(name="maxxansi"), args=args)

    def parse_expression(self) -> Expression:
        return self.parse_or()

    def parse_or(self) -> Expression:
        left = self.parse_and()
        while self.match(TokenType.OR):
            self.advance()
            right = self.parse_and()
            left = BinaryOp(left=left, op="or", right=right)
        return left

    def parse_and(self) -> Expression:
        left = self.parse_not()
        while self.match(TokenType.AND):
            self.advance()
            right = self.parse_not()
            left = BinaryOp(left=left, op="and", right=right)
        return left

    def parse_not(self) -> Expression:
        if self.match(TokenType.NOT):
            self.advance()
            return UnaryOp(op="not", operand=self.parse_not())
        if self.match(TokenType.AWAIT):
            self.advance()
            return Await(expression=self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self) -> Expression:
        left = self.parse_additive()
        while self.match(TokenType.EQEQ, TokenType.BANGEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE, TokenType.IN, TokenType.IS):
            op_tok = self.advance()
            op_map = {
                TokenType.EQEQ: "==",
                TokenType.BANGEQ: "!=",
                TokenType.LT: "<",
                TokenType.GT: ">",
                TokenType.LTE: "<=",
                TokenType.GTE: ">=",
                TokenType.IN: "in",
                TokenType.IS: "is",
            }
            right = self.parse_additive()
            left = BinaryOp(left=left, op=op_map[op_tok.type], right=right)
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
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.MOD, TokenType.SLASHSLASH):
            op_tok = self.advance()
            right = self.parse_unary()
            left = BinaryOp(left=left, op=op_tok.value, right=right)
        return left

    def parse_power(self) -> Expression:
        left = self.parse_postfix()
        if self.match(TokenType.STARSTAR):
            op_tok = self.advance()
            right = self.parse_unary()
            left = BinaryOp(left=left, op=op_tok.value, right=right)
        return left

    def parse_unary(self) -> Expression:
        if self.match(TokenType.MINUS):
            self.advance()
            operand = self.parse_unary()
            return BinaryOp(left=Number(0), op="-", right=operand)
        return self.parse_power()

    def parse_postfix(self) -> Expression:
        expr = self.parse_primary()
        while True:
            if self.match(TokenType.LPAREN):
                self.advance()
                args: List[Expression] = []
                if not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        self.advance()
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                expr = Call(func=expr, args=args)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                expr = Subscript(value=expr, index=index)
            elif self.match(TokenType.DOT):
                self.advance()
                attr_tok = self.expect(TokenType.IDENTIFIER)
                expr = Attribute(value=expr, attr=attr_tok.value)
            else:
                break
        return expr

    def parse_primary(self) -> Expression:
        if self.match(TokenType.STRING):
            tok = self.advance()
            return StringLiteral(value=tok.value)
        if self.match(TokenType.NUMBER):
            tok = self.advance()
            return Number(value=tok.value)
        if self.match(TokenType.TRUE):
            self.advance()
            return Boolean(value=True)
        if self.match(TokenType.FALSE):
            self.advance()
            return Boolean(value=False)
        if self.match(TokenType.NONE):
            self.advance()
            return NoneLiteral()
        if self.match(TokenType.PRINT):
            return self.parse_print_call()
        if self.match(TokenType.LBRACKET):
            self.advance()
            if self.match(TokenType.RBRACKET):
                self.advance()
                return ListLiteral(elements=[])
            
            first_expr = self.parse_expression()
            if self.match(TokenType.FOR):
                self.advance()
                var_tok = self.expect(TokenType.IDENTIFIER)
                self.expect(TokenType.IN)
                iterable = self.parse_expression()
                condition = None
                if self.match(TokenType.IF):
                    self.advance()
                    condition = self.parse_expression()
                self.expect(TokenType.RBRACKET)
                return ListComprehension(element=first_expr, target=var_tok.value, iterable=iterable, condition=condition)
            else:
                elements = [first_expr]
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACKET):
                        break
                    elements.append(self.parse_expression())
                self.expect(TokenType.RBRACKET)
                return ListLiteral(elements=elements)
        if self.match(TokenType.LBRACE):
            self.advance()
            if self.match(TokenType.RBRACE):
                self.advance()
                return Dictionary(keys=[], values=[])
            
            first_expr = self.parse_expression()
            if self.match(TokenType.COLON):
                self.advance()
                first_val = self.parse_expression()
                keys = [first_expr]
                values = [first_val]
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACE):
                        break
                    keys.append(self.parse_expression())
                    self.expect(TokenType.COLON)
                    values.append(self.parse_expression())
                self.expect(TokenType.RBRACE)
                return Dictionary(keys=keys, values=values)
            else:
                elements = [first_expr]
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RBRACE):
                        break
                    elements.append(self.parse_expression())
                self.expect(TokenType.RBRACE)
                return SetLiteral(elements=elements)
        if self.match(TokenType.IDENTIFIER):
            tok = self.advance()
            return Identifier(name=tok.value)
        if self.match(TokenType.LPAREN):
            self.advance()
            if self.match(TokenType.RPAREN):
                self.advance()
                return TupleLiteral(elements=[])
            expr = self.parse_expression()
            if self.match(TokenType.COMMA):
                elements = [expr]
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.RPAREN):
                        break
                    elements.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                return TupleLiteral(elements=elements)
            self.expect(TokenType.RPAREN)
            return expr

        self.diagnostics.raise_error("expected_expression", self.location())
        raise DiagnosticError(self.diagnostics.MESSAGES["expected_expression"], self.location())
