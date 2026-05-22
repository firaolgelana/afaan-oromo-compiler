"""Abstract Syntax Tree node definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

Statement = Union[
    "Assign",
    "If",
    "While",
    "ForLoop",
    "FunctionDef",
    "ClassDef",
    "Return",
    "ExprStmt",
    "Import",
    "TryStmt",
    "Break",
    "Continue",
    "Pass",
    "GlobalStmt",
    "NonlocalStmt",
    "Raise",
    "Assert",
    "Del",
    "Yield",
    "With",
]

Expression = Union[
    "Number",
    "Identifier",
    "Boolean",
    "NoneLiteral",
    "BinaryOp",
    "UnaryOp",
    "FunctionCall",
    "Await",
]


@dataclass
class Program:
    statements: List[Statement] = field(default_factory=list)


@dataclass
class Number:
    value: Union[int, float]


@dataclass
class Boolean:
    value: bool


@dataclass
class NoneLiteral:
    """homaa → None"""


@dataclass
class Identifier:
    name: str


@dataclass
class BinaryOp:
    left: Expression
    op: str
    right: Expression


@dataclass
class UnaryOp:
    op: str
    operand: Expression


@dataclass
class Await:
    expression: Expression


@dataclass
class Assign:
    name: str
    value: Expression


@dataclass
class ElifBranch:
    condition: Expression
    body: List[Statement]


@dataclass
class If:
    condition: Expression
    then_body: List[Statement]
    elif_branches: List[ElifBranch] = field(default_factory=list)
    else_body: Optional[List[Statement]] = None


@dataclass
class While:
    condition: Expression
    body: List[Statement]


@dataclass
class ForLoop:
    """marsaa (target in iterable) { body }"""
    target: str
    iterable: Expression
    body: List[Statement]


@dataclass
class FunctionDef:
    name: str
    params: List[str]
    body: List[Statement]
    is_async: bool = False


@dataclass
class ClassDef:
    name: str
    body: List[Statement]


@dataclass
class FunctionCall:
    name: str
    args: List[Expression]


@dataclass
class Return:
    value: Optional[Expression] = None


@dataclass
class ExprStmt:
    expression: Expression


@dataclass
class Import:
    """
    Import another .ao module.

    kind:
      'from_star' — fuudhu / irraa mod → from mod import *
      'import'    — fidi mod → import mod
    """
    module: str
    kind: str = "from_star"


@dataclass
class ExceptHandler:
    exc_type: Optional[str]
    body: List[Statement]


@dataclass
class TryStmt:
    body: List[Statement]
    handlers: List[ExceptHandler] = field(default_factory=list)
    finally_body: Optional[List[Statement]] = None


@dataclass
class Break:
    pass


@dataclass
class Continue:
    pass


@dataclass
class Pass:
    pass


@dataclass
class GlobalStmt:
    names: List[str]


@dataclass
class NonlocalStmt:
    names: List[str]


@dataclass
class Raise:
    expression: Optional[Expression] = None


@dataclass
class Assert:
    condition: Expression


@dataclass
class Del:
    target: Expression


@dataclass
class Yield:
    value: Optional[Expression] = None


@dataclass
class With:
    context: Expression
    body: List[Statement]
