"""
STATEMENT_LIST := { STATEMENT }
STATEMENT := <ASSINGNMENT | BINARY_EXPR | PRINT>
ASSIGNMENT :=  <ID> <EQUAL> <ID|DIGIT>
BINARY_EXPR := <ID | DIGIT> <SYMBOL> <ID | DIGIT>
PRINT_EXPR := <PRINT> <BINARY_EXPR | ID | DIGIT>
PRINT := “print”
EQUAL := “=”
SYMBOL := (“-”|”+”)
DIGIT  ::= ("0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9")
"""
from typing import List
import dataclasses


@dataclasses.dataclass
class BaseAST:
    pass


class StatementListAST(BaseAST):
    asts: List[BaseAST] = []

@dataclasses.dataclass
class BinaryExprAST(BaseAST):
    left: BaseAST
    right: BaseAST
    op: str


# ID
@dataclasses.dataclass
class VariableAST(BaseAST):
    name: str


@dataclasses.dataclass
class AssignmentAST(BaseAST):
    variable: VariableAST
    value: BaseAST


# PRINT
@dataclasses.dataclass
class PrintAST(BaseAST):
    arg: BaseAST


@dataclasses.dataclass
class DigitAST(BaseAST):
    value: int


@dataclasses.dataclass
class SymbolAST(BaseAST):
    value: str
