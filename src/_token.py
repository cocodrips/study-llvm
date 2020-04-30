import dataclasses
import enum


class TokenType(enum.Enum):
    TOK_IDENTIFIER = 1
    TOK_DIGIT = 2
    TOK_SYMBOL = 3
    TOK_INT = 4
    TOK_RETURN = 5
    TOK_EOF = 6


@dataclasses.dataclass
class Token:
    token_type: TokenType
    token_string: str
    number: int
    line: int


class TokenStream:
    tokens: list = []
    current_index: int = 1