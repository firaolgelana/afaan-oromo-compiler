"""Abstract Syntax Tree node definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union

# Statement types
Statement = Union[
    "Assign",
    "If",
    "While",
    "FunctionDef",
    "Return",
    "ExprStmt",
    "Import",
]

# Expression types
Expression = Union[
    "Number",
    "Identifier",
    "Boolean",
    "BinaryOp",
    "FunctionCall",
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
class Identifier:
    name: str


@dataclass
class BinaryOp:
    left: Expression
    op: str
    right: Expression


@dataclass
class Assign:
    name: str
    value: Expression


@dataclass
class If:
    condition: Expression
    then_body: List[Statement]
    else_body: Optional[List[Statement]] = None


@dataclass
class While:
    condition: Expression
    body: List[Statement]


@dataclass
class FunctionDef:
    name: str
    params: List[str]
    body: List[Statement]


@dataclass
class FunctionCall:
    name: str
    args: List[Expression]


@dataclass
class Return:
    value: Expression


@dataclass
class ExprStmt:
    """Expression used as a statement (e.g. maxxansi(x))."""
    expression: Expression


@dataclass
class Import:
    """Import another .ao file as a library (fuudhu)."""
    module: str
